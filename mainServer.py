import asyncio
import threading

# importaciones del proyecto
from src.websocket import API_ActorsServer
from src.utils import encontrar_producto_mas_barato


jsonPath= './src/paginasAScrapear.json'
eventoServer= threading.Event() # flag para detener el servidor de actores al final de la ejecucion

async def main(): # TODO: interfaz
    actorsServer= API_ActorsServer("127.0.0.1",8765, localServer= True, serverFlag= eventoServer)
    nombreProducto= input("que producto deseas buscar?: ")
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
    try:
        asyncio.run(main= main())
    finally:
        eventoServer.set() # detiene el servidor de actores local
        # sino no se apaga la terminal sigue funcionando hasta que se fuerza el cierre