import asyncio
from websockets.asyncio.server import serve, ServerConnection
import logging
from src import WebSocket_ActorServer

# Configuración específica para cada módulo
logging.getLogger('asyncio').setLevel(logging.WARNING)
logging.getLogger('pykka').setLevel(logging.WARNING)
logging.getLogger('websockets').setLevel(logging.INFO)

async def echo(websocket: ServerConnection):
  print(f"Echo server connected: {websocket.id}")
  async for message in websocket:
    await websocket.send(message)

async def start_actor_server():
  port = 8888
  event = asyncio.Event()
  
  # Iniciar WebSocket_ActorServer
  server = WebSocket_ActorServer(port=port, host="0.0.0.0", stop_flag=event)
  await server.serverLoop()

async def start_echo_server():
  # Servidor de prueba echo
  async with serve(echo, host="0.0.0.0", port=8889):
    print("Echo server running on port 8889")
    await asyncio.get_running_loop().create_future()  # Mantener el servidor corriendo

async def main():
  # Correr ambos servidores en paralelo
  await asyncio.gather(
    start_echo_server(),
    start_actor_server()
  )

if __name__ == "__main__":
  asyncio.run(main())
