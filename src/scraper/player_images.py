import logging
from asyncio import create_task, gather
from contextlib import contextmanager
from httpx import AsyncClient
from pathlib import Path
from os import listdir, mkdir
from selectolax.parser import HTMLParser
from shutil import rmtree

async def create_folder(player_name:str) -> str:
    """Create image folder for each player. Will re-create folder if already exists."""

    try:
        folder_path = Path.cwd().parent / f"data/raw/images/{player_name.replace(' ','_')}"
        mkdir(folder_path)
        logging.info(f"Folder created at: {folder_path}")
        return folder_path
    except FileExistsError as e:
        rmtree(folder_path)
        mkdir(folder_path)
        logging.info(f"Folder re-created at: {folder_path}")
        return folder_path

async def get_image_urls(player_name:str):
    """Scrapes all available image URLs from Getty Images for the provided player"""

    full_name = player_name.split(" ")
    first_name = full_name[0]
    last_name = full_name[1]
    target_url = f"https://www.gettyimages.com/search/2/image?phrase={first_name}%20{last_name}" + \
                    "%20football&sort=mostpopular&license=rf%2Crm&compositions=portrait"
    logging.info(f"Scrapping image at: {target_url}")

    async with AsyncClient() as client:
        response = await client.request("GET", target_url)
        image_url_list = HTMLParser(response.text).css("figure > picture > img")
        image_urls = [image_url.attributes.get("src") for image_url in image_url_list]
        logging.info(f"Total images found for {player_name}: {len(image_urls)}")
        return image_urls
    
async def download_image(player_name:str,player_image_url:str,player_image_folder_path:str):
    """Download and store the image from the provided Getty URL"""
    
    image_number = len(listdir(player_image_folder_path))
    image_path = player_image_folder_path / f"{player_name}_{image_number}.jpg"

    async with AsyncClient() as client:
        response = await client.request("GET", player_image_url)
        with open(image_path, "wb") as file:
            file.write(response.content)

async def create_folder_get_urls_download_images(player_name:str) -> None:
    """Composite function that combines creating folders, get image urls, and download images"""

    player_image_folder_path = await create_folder(player_name)
    player_image_urls = await get_image_urls(player_name)
    download_player_images_tasks = [create_task(
                                        download_image(player_name,
                                                       player_image_url,
                                                       player_image_folder_path)) 
                                        for player_image_url in player_image_urls[:10]] 
    await gather(*download_player_images_tasks)
