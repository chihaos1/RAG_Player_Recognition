from asyncio import gather, run
from dataclasses import dataclass
from utils.logging.decorator import log
from utils.scrapping.scrape_players import wikipedia_player_scrape

@dataclass
class Options:
    scrape: bool = False

@log
async def entrypoint():
    response = await gather(wikipedia_player_scrape())
    return response

def main():
    run(entrypoint())

if __name__ == "__main__":
    # main()
    main()