from asyncio import create_task, gather, run
from dataclasses import dataclass
from dotenv import load_dotenv, find_dotenv
from os import getenv
from embedder.image_embeddings import embed_player_images, upload_to_pinecone 
from embedder.setup_pinecone import create_pinecone_index, initialize_pinecone
from scraper.player_names import get_player_names
from scraper.player_images import get_player_images
from utils.logger import log

@dataclass
class ScrapeOptions:
    scrape: bool = True
    player_scrape_limit: int = 10
    player_image_scrape_limit: int = 5

@dataclass
class EmbedOptions:
    create_index: bool = False

@log
async def scrape_images(options: ScrapeOptions) -> None:
    """Scrapes the player images"""

    player_names = await get_player_names(options.player_scrape_limit)
    get_player_images_tasks = [
        create_task(get_player_images(player_name,options.player_image_scrape_limit)) 
        for player_name in player_names] 
    await gather(*get_player_images_tasks)

@log
async def prepare_images(options: EmbedOptions, index_name: str, api_key: str):
    """Loads, embeds, then uploads player images to Pinecone"""
    
    pinecone = initialize_pinecone(api_key)
    if options.create_index:
        create_pinecone_index(index_name,pinecone)
    index = pinecone.Index(index_name)
    image_embeddings = await embed_player_images(index)
    await upload_to_pinecone(image_embeddings,index)
    

if __name__ == "__main__":
    load_dotenv(find_dotenv())
    PINECONE_API_KEY = getenv("PINECONE_API_KEY")
    INDEX_NAME = "player-images"
    
    scrape_options = ScrapeOptions(
        scrape = False,
        player_scrape_limit=10, 
        player_image_scrape_limit=5
    )

    embed_options = EmbedOptions(
        create_index = True
    )

    if scrape_options.scrape:
        run(scrape_images(scrape_options))
    
    run(prepare_images(embed_options,INDEX_NAME,PINECONE_API_KEY))
    
