from asyncio import create_task, gather, run
from dataclasses import dataclass
from scraper.player_names import get_player_names
from scraper.player_images import create_folder_get_urls_download_images
from utils.logger import log

@dataclass
class Options:
    scrape: bool = False

@log
async def entrypoint():
    player_names = await get_player_names()
    scrape_player_images_tasks = [create_task(create_folder_get_urls_download_images(player_name)) 
                                  for player_name in player_names[:1]] 
    player_images = await gather(*scrape_player_images_tasks)

def main():
    run(entrypoint())

if __name__ == "__main__":
    main()