import asyncio
from websockets.asyncio.server import serve, ServerConnection
import logging
from src import WebSocket_ActorServer

# Configuración específica para cada módulo
logging.getLogger('asyncio').setLevel(logging.WARNING)
logging.getLogger('pykka').setLevel(logging.WARNING)
logging.getLogger('websockets').setLevel(logging.INFO)


async def run_server(event):
    port = 8765
    server = WebSocket_ActorServer(port=port, host="0.0.0.0", stop_flag=event)
    
    try:
        await server.serverLoop()
    except asyncio.CancelledError:
        pass
    finally:
        # Ensure that the server services are stopped
        await server.stopServerServices()
    
def main():
    event = asyncio.Event()
    try:
        asyncio.run(run_server(event))
    except KeyboardInterrupt:
        print("Ctrl+c recibido, detendiendo servidor...")
        event.set()
    finally:
        print("Servidor detenido.")

if __name__ == "__main__":
    main()
