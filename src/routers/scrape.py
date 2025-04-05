from fastapi import APIRouter
from scraper.player_names import get_player_names
from scraper.player_images import get_player_images

router = APIRouter( 
    prefix="/scrape",
    tags=["scrape"]
) 

async def scrape_images(team_name: str) -> None:
    """Scrapes the player images"""

    player_names = await get_player_names(team_name)
    get_player_images_tasks = [
        create_task(get_player_images(player_name,options.player_image_scrape_limit)) 
        for player_name in player_names] 
    await gather(*get_player_images_tasks)

@router.post("/scrape-images")
async def scrape_player_images(team_name: str):
