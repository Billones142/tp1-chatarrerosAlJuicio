import websockets
import json
from typing import Literal
import logging

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

class API_ActorsServer:
    def __init__(self, uri: str):
        self.uri = uri
        self.serverWebsocketConnection = None
    
    async def __aenter__(self):
        await self.connect()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.disconnect()
    
    async def connect(self):
        try:
            self.serverWebsocketConnection = await websockets.connect(self.uri)
        except:
            raise Exception("Error al conectarse al servidor")
    
    async def disconnect(self):
        if self.serverWebsocketConnection:
            try:
                await self.serverWebsocketConnection.close()
                print("Conexión WebSocket cerrada")
            except:
                print("error al cerrar coneccion")
    
    async def ask_scrapper(self, url: str):
        if self.serverWebsocketConnection:
            await self.serverWebsocketConnection.send(json.dumps({
                "commandWebSocket": "scrapeHtml",
                "url": url
            }))
        else:
            raise Exception("asked before conecting to websocket server")

        # Recibir respuesta del servidor
        response = await self.serverWebsocketConnection.recv()
        return json.loads(response)

    async def ask_parser(self, *, command: Literal["parseMercadoLibre", "parseUranostream", "parseHardgamers"], productName: str, htmlString: str):
        """Envía una solicitud al parser actor para analizar el HTML."""
        await self.serverWebsocketConnection.send(json.dumps({
            "commandWebSocket": "parseHtml",
            "command": command,
            "productName": productName,
            "htmlString": htmlString
        }))

        # Recibir respuesta del servidor
        response = await self.serverWebsocketConnection.recv()

        # Se espera como respuesta un string del HTML procesado
        return json.loads(response)