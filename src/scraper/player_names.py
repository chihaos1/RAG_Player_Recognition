import logging
from httpx import AsyncClient
from selectolax.parser import HTMLParser
from typing import List

#SCRAPE PLAYERS NAME
async def get_player_names(player_scrape_limit: int) -> List[str]:
    """Scrapes player names from Wikipedia"""
    
    async with AsyncClient() as client:
        squad_url = "https://en.wikipedia.org/wiki/2024–25_Newcastle_United_F.C._season"
        response = await client.request("GET", squad_url)
        players = HTMLParser(response.text).css("td.fn")
        squad = [player.text().strip() for player in players]
        logging.info(f"Squad scraped: {squad[:player_scrape_limit]}")
        return squad[:player_scrape_limit]

    