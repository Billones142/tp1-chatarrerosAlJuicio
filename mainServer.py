#from .src.utils.jsonParse import parsePaginasJson
#from .src.actors.scrapping.scrappingActor import ScraperActor
#from typing import Tuple
import asyncio

from src.websocket import API_ActorsServer
#import Pyro5.api
#import time

jsonPath= 'paginasAScrapear.json'

async def main(): # TODO: interfaz
  async with API_ActorsServer(f"ws://127.0.0.1:{8765}") as serverActores:
    response= await serverActores.ask_scrapper("https://youtube.com") # elegido por su complejidad y longitud
    print("respuesta:",response)

if __name__ == '__main__':
  asyncio.run(main= main())