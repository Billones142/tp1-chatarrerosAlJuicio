import websockets
import json
from typing import Literal


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

    async def ask_parser(self, *, command: Literal["parseMercadoLibre", "parseUranostream", "parseHardgamers"], htmlString: str):
        """Envía una solicitud al parser actor para analizar el HTML."""
        await self.serverWebsocketConnection.send(json.dumps({
            "commandWebSocket": "parseHtml",
            "command": command,
            "htmlString": htmlString
        }))

        # Recibir respuesta del servidor
        response = await self.serverWebsocketConnection.recv()

        # Se espera como respuesta un string del HTML procesado
        return json.loads(response)