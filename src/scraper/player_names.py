import logging
from unidecode import unidecode
from httpx import AsyncClient
from selectolax.parser import HTMLParser
from typing import List

async def get_player_names(team_name: str) -> List[str]:
    """Scrapes player names from Wikipedia"""

    async with AsyncClient() as client:
        squad_url = f"https://en.wikipedia.org/wiki/2024–25_{team_name}_F.C._season"
        response = await client.request("GET", squad_url)
        players = HTMLParser(response.text).css("td.fn")
        squad = [unidecode(player.text().strip()) for player in players]
        logging.info(f"Squad scraped: {squad}")
        return squad