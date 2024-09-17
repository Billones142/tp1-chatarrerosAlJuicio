import asyncio

# importaciones del proyecto
from src.websocket import API_ActorsServer
from src.utils import encontrar_producto_mas_barato


jsonPath= './src/paginasAScrapear.json'


async def main(): # TODO: interfaz
    nombreProducto= "4060"
    actorsServer= API_ActorsServer(f"ws://127.0.0.1:{8765}")
    async with actorsServer:
        htmlString= await actorsServer.ask_scrapper(f"https://listado.mercadolibre.com.ar/nuevo/{nombreProducto}")
        htmlParseado= await actorsServer.ask_parser(command= "parseMercadoLibre", htmlString=htmlString, productName=nombreProducto)
        htmlString2= await actorsServer.ask_scrapper(f"https://uranostream.com/?s={nombreProducto}&post_type=product&dgwt_wcas=1")
        htmlParseado2= await actorsServer.ask_parser(command= "parseUranostream", htmlString=htmlString2, productName=nombreProducto)
        htmlString3= await actorsServer.ask_scrapper(f"https://www.hardgamers.com.ar/search?text={nombreProducto}")
        htmlParseado3= await actorsServer.ask_parser(command= "parseHardgamers", htmlString=htmlString3, productName=nombreProducto)
    
    print(encontrar_producto_mas_barato(htmlParseado))
    print(encontrar_producto_mas_barato(htmlParseado2))
    print(encontrar_producto_mas_barato(htmlParseado3))

if __name__ == '__main__':
    asyncio.run(main= main())