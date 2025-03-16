import logging
from httpx import AsyncClient
from selectolax.parser import HTMLParser

async def get_player_names() -> list[str]:
    """Scrapes player names from Wikipedia"""
    
    def process_names(name:str) -> str:
        """Helper function of get_player_names. \
            Concatenate last names with space for image searchings later"""

        name_parts = name.split()
        if len(name_parts) > 2:
            concat_lname = "".join(name_parts[1:])
            return " ".join([name_parts[0],concat_lname])
        else:
            return name
        
    async with AsyncClient() as client:
        squad_url = "https://en.wikipedia.org/wiki/2012-13_Newcastle_United_F.C._season"
        response = await client.request("GET", squad_url)
        players = HTMLParser(response.text).css("td.fn")
        squad = [process_names(player.text().strip()) for player in players]
        logging.info(f"Squad scraped: {squad}")
        return squad

    