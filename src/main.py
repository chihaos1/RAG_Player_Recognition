from asyncio import create_task, gather, run
from dataclasses import dataclass
from dotenv import load_dotenv, find_dotenv
from os import getenv
from embedder.image_embeddings import embed_player_images, upload_to_pinecone 
from pathlib import Path
from querier.image_query import query_pinecone
from scraper.player_names import get_player_names
from scraper.player_images import get_player_images
from utils.logger import log
from utils.pinecone import create_pinecone_index, initialize_pinecone

@dataclass
class ScrapeOptions:
    scrape: bool = True
    player_scrape_limit: int = 10
    player_image_scrape_limit: int = 5

@dataclass
class EmbedOptions:
    create_index: bool = False
    embed: bool = False

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

@log
async def query_images(index_name: str, api_key: str):
    """Queries Pinecone to identify the player in the uploaded image"""

    pinecone = initialize_pinecone(api_key)
    index = pinecone.Index(index_name)
    query_image_path = Path.cwd().parent / "data" / "query" / "Tonali.jpg"
    
    results = await query_pinecone(query_image_path,index,top_k=3)
    print(results)
    
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
        embed = False,
        create_index = True
    )

    if scrape_options.scrape:
        run(scrape_images(scrape_options))
    
    if embed_options.embed:
        run(prepare_images(embed_options,INDEX_NAME,PINECONE_API_KEY))

    run(query_images(INDEX_NAME, PINECONE_API_KEY))
    
