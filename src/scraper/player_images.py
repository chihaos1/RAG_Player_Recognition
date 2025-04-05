import aiofiles
import logging
import re
from httpx import AsyncClient
from pathlib import Path
from selectolax.parser import HTMLParser
from shutil import rmtree
from typing import AsyncGenerator, List

#CREATE FOLDER
async def _create_folder_path(player_name: str) -> Path:
    """Generates the folder path that will store the player images (helper function)"""
    return Path.cwd().parent / f"data/images/{player_name.replace(' ','_')}"

async def create_folder(player_name: str) -> str:
    """Create image folder for each player. Will re-create folder if already exists."""

    folder_path = await _create_folder_path(player_name)
    if folder_path.exists():
        rmtree(folder_path)
    folder_path.mkdir(parents=True, exist_ok=True)
    logging.info(f"Folder created at: {folder_path}")
    
    return folder_path

#SCRAPE PLAYER IMAGES
async def _build_url(player_name: str) -> str:
        """Builds the Getty URL for the player (helper function)"""

        full_name = player_name.split(" ")
        query = "%20".join(full_name)
        return "https://www.gettyimages.com/search/2/image?compositions=portrait&numberofpeople=one&" + \
                f"phrase={query}%20football&sort=mostpopular&license=rf%2Crm&compositions=portrait"

async def get_image_urls(player_name: str) -> List[str]:
    """Scrapes all available image URLs from Getty Images for the provided player"""

    async with AsyncClient() as client:
        try:
            response = await client.request("GET", await _build_url(player_name))
        except Exception as e:
            logging.error(f"Failed to fetch image URLs for {player_name}: {e}")
            return []

        image_url_list = HTMLParser(response.text).css("figure > picture > img")
        image_urls = [image_url.attributes.get("src") for image_url in image_url_list]
        logging.info(f"Total images found for {player_name}: {len(image_urls)}")
        return image_urls

#DOWNLOAD IMAGES
async def _async_generate_url(
                image_url_list: List[str], 
                player_image_scrape_limit: int) -> AsyncGenerator:
    """Generates the image urls of the player asynchronously (internal function)"""

    for image_url in image_url_list[:player_image_scrape_limit]:
        yield image_url

async def download_image(player_image_url: str,
                         player_image_folder_path: str) -> None:
    """Downloads and stores the image locally from the provided Getty URL"""

    async with AsyncClient() as client:
        try: 
            response = await client.request("GET", player_image_url, timeout=10)
        except Exception as e:
            logging.error(f"Failed to download image {player_image_url}: {e}")
            return None

        async with aiofiles.open(player_image_folder_path, "wb") as image:
            logging.info(f"Storing image at: {player_image_folder_path}")
            await image.write(response.content)

#COMPOSITE
async def get_player_images(player_name: str, player_image_scrape_limit: int) -> None:
    """Composite function that combines create folders, get image urls, and download images"""

    player_image_folder_path = await create_folder(player_name)
    player_image_urls = await get_image_urls(player_name)

    if not player_image_urls:
        logging.warning(f"No images found for {player_name}. Skipping download.")
        return

    async for player_image_url in _async_generate_url(player_image_urls,player_image_scrape_limit):
        match = re.search(r"id/(\d+)/", player_image_url) #Get the unique index of the image
        if not match:
            logging.warning(f"Skipping invalid image URL: {player_image_url}")
            continue

        player_image_index = match.group(1)
        player_image_path = player_image_folder_path / f"{player_name}_{player_image_index}.jpg"

        await download_image(player_image_url,player_image_path)

