import asyncio
import threading
import time
import websockets
import json
from typing import Literal, TypedDict
import logging

from src.websocket.ActorsServer import WebSocket_ActorServer

nombreLogger= "API_ActorsServer"

# Configura el logger del módulo
logger = logging.getLogger(nombreLogger)  # Nombre del logger igual al nombre del módulo
logger.setLevel(logging.NOTSET)  # Establece el nivel de logging

# Configurar el formato de los mensajes de log
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Crear y agregar un manejador para la consola
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

# Añadir el manejador al logger
logger.addHandler(console_handler)

class precioYLinks(TypedDict):
    price: int
    link: str

def startActorServer(host: str, port: int, stopFlag):
    server = WebSocket_ActorServer(port=port,host= host, stop_flag=stopFlag)
    loop = asyncio.new_event_loop()  # Crear un nuevo event loop para este thread
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(server.serverLoop())  # Ejecuta hasta que la stopFlag cambie
    finally:
        loop.close()  # Cerrar el event loop cuando termina

class ErrorActoresAPI(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message

class API_ActorsServer:
    """
    A class used to connect with the actors server

    Attributes
    ----------
    host : str
        ip or url that points where the actors server in hosted
    port: int
        indicates the port the actors server is using
    localServer : bool
        if true a server will be hosted in another thread
    serverFlag : threading.Event
        a flag that if set will stop the local server

    Methods
    -------
    ask_scrapper(url: str)
        async function that asks the actor server to download the html of the url provided
    ask_parser(*, 
            command: Literal["parseMercadoLibre", "parseUranostream", "parseHardgamers"],
            productName: str,
            htmlString: str)
            -> list[precioYLinks]
        async function that asks the actor server to parse a url of the supported pages extracting
        the prices and links of a product and returning them in a list
    """
    def __init__(self, host= "127.0.0.1", port= 8765, *, localServer= False, serverFlag= threading.Event()):
        self.uri = f"ws://{host}:{port}"
        if localServer:
            self.serverFlag= serverFlag
            self.actor_server_thread = threading.Thread(target=startActorServer, args=(host, port, self.serverFlag), name="loop del servidor")
            self.actor_server_thread.daemon = True
            self.actor_server_thread.start()
            logging.getLogger("WebSocket_ActorServer").setLevel(logging.ERROR)
            time.sleep(2)  # Espera que el servidor arranque
    
    async def __aenter__(self):
        await self.connect()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.disconnect()
    
    async def connect(self):
        try:
            self.serverWebsocketConnection = await websockets.connect(self.uri)
        except:
            raise ErrorActoresAPI("Error al conectarse al servidor")
    
    async def disconnect(self):
        if self.serverWebsocketConnection:
            try:
                await self.serverWebsocketConnection.close()
                print("Conexión WebSocket cerrada")
            except:
                print("error al cerrar coneccion")
    
    async def ask_scrapper(self, url: str) -> str:
        if self.serverWebsocketConnection:
            await self.serverWebsocketConnection.send(json.dumps({
                "commandWebSocket": "scrapeHtml",
                "url": url
            }))
        else:
            raise ErrorActoresAPI("asked before conecting to websocket server")

        # Recibir respuesta del servidor
        response = await self.serverWebsocketConnection.recv()

        jsonCargado= json.loads(response)

        if len(jsonCargado["error"]) != 0:
            raise ErrorActoresAPI(jsonCargado["error"])

        return jsonCargado["result"]

    async def ask_parser(self, *, command: Literal["parseMercadoLibre", "parseUranostream", "parseHardgamers"], productName: str, htmlString: str) -> list[precioYLinks]:
        """Envía una solicitud al parser actor para analizar el HTML."""
        await self.serverWebsocketConnection.send(json.dumps({ # TODO en caso de error hacer un raise de error en el servidor
            "commandWebSocket": "parseHtml",
            "command": command,
            "productName": productName,
            "htmlString": htmlString
        }))

        # Recibir respuesta del servidor
        response = await self.serverWebsocketConnection.recv()

        jsonCargado= json.loads(response)

        if len(jsonCargado["error"]) != 0:
            raise ErrorActoresAPI(jsonCargado["error"])

        # Se espera como respuesta un string del HTML procesado
        return json.loads(json.loads(jsonCargado["result"]))