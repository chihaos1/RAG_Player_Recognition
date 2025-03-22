import logging
import unicodedata
from httpx import AsyncClient
from selectolax.parser import HTMLParser
from typing import List

#SCRAPE PLAYERS NAME
async def _normalize_name(player_name:str):
    """Normalize player name to ASCII"""
    return unicodedata.normalize("NFKD", player_name).encode('ascii', errors='ignore').decode('ascii')

async def get_player_names(player_scrape_limit: int) -> List[str]:
    """Scrapes player names from Wikipedia"""
    
    async with AsyncClient() as client:
        squad_url = "https://en.wikipedia.org/wiki/2024–25_Newcastle_United_F.C._season"
        response = await client.request("GET", squad_url)
        players = HTMLParser(response.text).css("td.fn")
        squad = [await _normalize_name(player.text().strip()) for player in players]
        logging.info(f"Squad scraped: {squad[:player_scrape_limit]}")
        return squad[:player_scrape_limit]

    