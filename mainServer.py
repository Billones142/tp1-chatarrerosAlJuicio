import asyncio

# importaciones del proyecto
from src.websocket import API_ActorsServer


jsonPath= 'paginasAScrapear.json'

async def main(): # TODO: interfaz
    actorsServer= API_ActorsServer(f"ws://127.0.0.1:{8765}")
    async with actorsServer:
        response= await actorsServer.ask_scrapper("https://youtube.com") # elegido por su complejidad y longitud
        print("respuesta:",response)
        

if __name__ == '__main__':
    asyncio.run(main= main())