import asyncio
import websockets
import json

from src.actors.scrapping.scrappingActor import ScraperActor
from src.actors.parse.parseActor import ParseActor

stop_flag = False

def start_actor_scrapper(self, url: str):
  actor_ref = ScraperActor.start()
  result = actor_ref.ask(block= True, message={'command': 'scrapeHtml', 'url': url})
  actor_ref.stop()
  return str(result)


def start_actor_HtmlParser(self, comand: str, htmlString: str):
  actor_ref = ParseActor.start()
  result = actor_ref.ask(block= True, message={'command': comand, 'htmlString': htmlString})
  actor_ref.stop()
  return result

async def handle_client(websocket: websockets.WebSocketClientProtocol):
  try:
    while True:
      message= await websocket.recv()
      response= await handle_message(message)
      await websocket.send(response)
  except websockets.exceptions.ConnectionClosed as conectionClosed:
    print("Error: conexion cerrada")


async def handle_message(message):
  send= ""
  try:
    messages = json.loads(message)
  except Exception as e:
    send= str(e) #"Error, mensaje no valido"
  
  try:
    if messages["commandWebSocket"] == "scrapeHtml":
      send= start_actor_scrapper(messages["url"])
    elif messages["commandWebSocket"] == "parseHtml":
      send= json.dump(start_actor_HtmlParser(messages["command"], messages["htmlString"]))
  except:
    send= "error de actores"
  return send

async def serverLoop(port: int, stop_flag: asyncio.Event= asyncio.Event()):
    async with websockets.serve(handle_client, "localhost", port):
        while not stop_flag.is_set():
            await asyncio.sleep(1)

def serverStart(port: int, stop_flag: asyncio.Event):
  asyncio.run(serverLoop(port= port, stop_flag= stop_flag))