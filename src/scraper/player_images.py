import logging
from functools import reduce
from pathlib import Path
from os import mkdir
from shutil import rmtree
from typing import Callable

async def scrape_player_images(player_name:str):
    """Scrapes player images from Getty Images"""

    full_name = player_name.split(" ")
    first_name = full_name[0]
    last_name = full_name[1]
    image_url = f"https://www.gettyimages.com/search/2/image?phrase={first_name}%20{last_name}" + \
                    "%20football%20newcastle&sort=mostpopular&license=rf%2Crm&compositions=portrait"
    logging.info(f"Scraped image at: {image_url}")

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
    await scrape_player_images(player_name)