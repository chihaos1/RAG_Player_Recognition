import asyncio
from enum import Enum
from fastapi import APIRouter, Query
from scraper.player_names import get_player_names
from scraper.player_images import get_player_images
from starlette import status

router = APIRouter( 
    prefix="/scrape",
    tags=["scrape"]
) 

class TeamOptions(str, Enum):
    newcastle = "Newcastle_United"
    west_ham = "West_Ham_United"
    brighton = "Brighton_%26_Hove_Albion"

@router.get("/", status_code=status.HTTP_200_OK)
async def scrape_player_images(team_name: TeamOptions = Query(...), image_per_player:int = 5) -> dict[str,int]:

    player_names = await get_player_names(team_name.value)
    get_player_images_tasks = [
        asyncio.create_task(get_player_images(player_name, image_per_player)) 
        for player_name in player_names[:3]] 
    results = await asyncio.gather(*get_player_images_tasks)
    scrape_results = {name: image_count for name, image_count in results}

    return scrape_results