from asyncio import create_task, gather, run
from dataclasses import dataclass
from dotenv import load_dotenv, find_dotenv
from embedder.image_embeddings import embed_player_images, upload_to_pinecone 
from os import getenv
from pathlib import Path
from querier.image_query import query_openai,query_pinecone
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
    image_embeddings = await embed_player_images()
    await upload_to_pinecone(image_embeddings,index)

@log
async def query_images(index_name: str, pinecone_api_key: str):
    """Queries Pinecone to identify the player in the uploaded image"""

    pinecone = initialize_pinecone(pinecone_api_key)
    index = pinecone.Index(index_name)
    query_image_path = Path.cwd().parent / "data" / "query" / "Tonali.jpg" #Path to the image user wants to query
    
    player_name = await query_pinecone(query_image_path,index,top_k=1) #Queries PC for most similar player
    llm_response = await query_openai(player_name) #Queries LLM for the player's career and playstyle
    print(llm_response)

from fastapi import FastAPI
from routers import query

app = FastAPI()
app.include_router(query.router)

if __name__ == "__main__":
    load_dotenv(find_dotenv())
    PINECONE_API_KEY = getenv("PINECONE_API_KEY")
    PINECONE_INDEX_NAME = "player-images"
    OPENAI_API_KEY = getenv("OPENAI_API_KEY")
    
    scrape_options = ScrapeOptions(
        scrape = False,
        player_scrape_limit=10, 
        player_image_scrape_limit=5
    )

    embed_options = EmbedOptions(
        embed = False,
        create_index = False
    )

    if scrape_options.scrape: #If scraping is needed
        run(scrape_images(scrape_options))
    
    if embed_options.embed: #If embedding data is needed
        run(prepare_images(embed_options,PINECONE_INDEX_NAME,PINECONE_API_KEY))

    run(query_images(PINECONE_INDEX_NAME,PINECONE_API_KEY))
    
