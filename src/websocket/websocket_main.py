import asyncio
import websockets
import json
from typing import Literal
import logging

class Comunication_WebSocket_ActorsServer:
  def __init__(self, uri: str):
    self.uri = uri
    self.serverWebsocketConnection = None

  async def __aenter__(self):
    """Método de entrada para el contexto asincrónico (abre la conexión)."""
    await self.connect()
    return self

  async def __aexit__(self, exc_type, exc_val, exc_tb):
    """Método de salida para el contexto asincrónico (cierra la conexión)."""
    await self.disconnect()

  async def connect(self):
    self.serverWebsocketConnection = await websockets.connect(self.uri)
    print("Conexión WebSocket establecida")

  async def disconnect(self):
    if self.serverWebsocketConnection:
      await self.serverWebsocketConnection.close()
      print("Conexión WebSocket cerrada")

  async def ask_scrapper_actor(self, url: str):
    if self.serverWebsocketConnection:
      await self.serverWebsocketConnection.send(json.dumps({
        "commandWebSocket": "scrapeHtml",
        "url": url
      }))
    else:
      raise Exception("asked before conecting to websocket server")
    
    # Recibir respuesta del servidor
    response = await self.serverWebsocketConnection.recv()
    return response
    
  async def ask_parser_actor(self, *, command: Literal["parseMercadoLibre", "parseUranostream", "parseHardgamers"], htmlString: str):
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