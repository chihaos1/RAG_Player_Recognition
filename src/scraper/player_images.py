import logging
from httpx import AsyncClient
from pathlib import Path
from os import mkdir
from selectolax.parser import HTMLParser
from shutil import rmtree

async def get_image_urls(player_name:str):
    """Scrapes all available image URLs from Getty Images for the provided player"""

    full_name = player_name.split(" ")
    first_name = full_name[0]
    last_name = full_name[1]
    target_url = f"https://www.gettyimages.com/search/2/image?phrase={first_name}%20{last_name}" + \
                    "%20football&sort=mostpopular&license=rf%2Crm&compositions=portrait"
    logging.info(f"Scraped image at: {target_url}")

    async with AsyncClient() as client:
        response = await client.request("GET", target_url)
        image_url_list = HTMLParser(response.text).css("figure > picture > img")
        print(image_url_list)
        image_urls = [image_url.attributes.get("src") for image_url in image_url_list]
        logging.info(f"Image URLS for {player_name}: {image_urls}")
        return image_urls

async def create_folder(player_name:str) -> None:
    """Create image folder for each player. Will re-create folder if already exists"""

    try:
        folder_path = Path.cwd().parent / f"data/raw/images/{player_name.replace(" ","_")}"
        mkdir(folder_path)
        logging.info(f"Folder created at: {folder_path}")
    except FileExistsError as e:
        rmtree(folder_path)
        mkdir(folder_path)
        logging.info(f"Folder re-created at: {folder_path}")

async def create_folder_scrape_images(player_name:str) -> None:
    """Composite function that combines creating folders and scraping images"""

    await create_folder(player_name)
    await get_image_urls(player_name)