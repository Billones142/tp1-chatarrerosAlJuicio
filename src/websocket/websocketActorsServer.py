#import websockets
from websockets.asyncio.server import serve, ServerConnection
import asyncio
import json
import time


from src.actors import ScraperActor, ParseActor


class WebSocket_ActorServer(): #perdon gaby, es mas facil cuando es una clase
  def __init__(self, port: int, host: str= "localhost", stop_flag: asyncio.Event= asyncio.Event()):
    self.host= host
    self.port= port
    self.stop_flag= stop_flag

  async def startServer(self):
    self.scrapperActor= ScraperActor.start()
    self.parseActor= ParseActor.start()
    try:
      self.websocketServer= await serve(handler= self.handle_client, host= self.host, port= self.port)
    except Exception as e:
      self.scrapperActor.stop(block= True)
      self.parseActor.stop(block= True)
      raise Exception("Error al iniciar websocket:\n" + e)
  
  async def stopServerServices(self):
    self.websocketServer.close()
    await self.websocketServer.wait_closed()
    self.scrapperActor.stop(block= True)
    self.parseActor.stop(block= True)

  """async def handle_client(self, websocket: websockets.WebSocketClientProtocol):
    try:
      while not self.stop_flag.is_set(): # mientras este evento no este activo recibir mensajes
        message= await websocket.recv() # espera un mensaje
        response= await self.handle_message(message) # responde el mensaje
        await websocket.send(response) # envia la respuesta
    except websockets.exceptions.ConnectionClosed as conectionClosed:
      print("Error: conexion cerrada")
      return
    except:
      await self.stopServerServices()
      return"""
  
  async def handle_client(self,websocket: ServerConnection):
    async for message in websocket:
      response= await self.handle_message(message) # responde el mensaje
      await websocket.send(response) # envia la respuesta

  async def handle_message(self,message):
    response= ""
    error= ""
    try:
      messages = json.loads(message)
      if messages["commandWebSocket"] == "scrapeHtml":
        response= self.ask_scrapper(url= messages["url"])
      elif messages["commandWebSocket"] == "parseHtml":
        response= json.dumps(self.ask_HtmlParser(messages["command"], messages["htmlString"]))
    except Exception as e:
      error= "Error del servidor:\n" + str(e) + "\n Fin de error del servidor"
    return json.dumps({"error": error,"result":response})

  def ask_scrapper(self,url: str) -> str:
    return self.scrapperActor.ask(block= True, message={'command': 'scrapeHtml', 'url': url})

  def ask_HtmlParser(self, comand: str, htmlString: str) -> list:
    return self.parseActor.ask(block= True, message={'command': comand, 'htmlString': htmlString})

  async def serverLoop(self):
    await self.startServer()
    while not self.stop_flag.is_set():
      await asyncio.sleep(1)
    print("apagando\n")
    await self.stopServerServices()