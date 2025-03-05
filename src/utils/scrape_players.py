from asyncio import gather, run
from httpx import AsyncClient
from selectolax.parser import HTMLParser
# from typing import

async def wikipedia_player_scrape() -> list[str]:
    
    async with AsyncClient() as client:
        url = "https://en.wikipedia.org/wiki/2012%E2%80%9313_Newcastle_United_F.C._season#Players"
        response = await client.request("GET", url)
        players = HTMLParser(response.text).css("td.fn")
        squad = [await name_processing(player.text().strip()) for player in players]
        print(squad)
        return squad

async def name_processing(player:str):
    """Concatenate last names for image searchings later"""

    player_name = player.split()
    if len(player_name) > 2:
        concat_lname = "".join(player_name[1:])
        return " ".join([player_name[0],concat_lname])
    else:
        return player


# https://www.gettyimages.com/search/2/image?phrase=romain%20amalfitano&sort=mostpopular&license=rf%2Crm&compositions=portrait

async def entrypoint():
    response = await gather(wikipedia_player_scrape())

def main():
    run(entrypoint())

if __name__ == "__main__":
    main()