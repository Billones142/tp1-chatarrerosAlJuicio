import asyncio

# importaciones del proyecto
from src.websocket import API_ActorsServer
from src import utils


jsonPath= 'paginasAScrapear.json'

async def main(): # TODO: interfaz
    actorsServer= API_ActorsServer(f"ws://127.0.0.1:{8765}")
    async with actorsServer:
        htmlString= await actorsServer.ask_scrapper("https://listado.mercadolibre.com.ar/2060#D[A:2060]") # elegido por su complejidad y longitud
        htmlParseado= await actorsServer.ask_parser(command= "parseMercadoLibre", htmlString=htmlString, productName="2060")
    print(htmlParseado)

if __name__ == '__main__':
    asyncio.run(main= main())