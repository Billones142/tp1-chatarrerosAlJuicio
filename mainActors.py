import asyncio
from websockets.asyncio.server import serve, ServerConnection
import logging
from src import WebSocket_ActorServer

# Configuración específica para cada módulo
logging.getLogger('asyncio').setLevel(logging.WARNING)
logging.getLogger('pykka').setLevel(logging.WARNING)
logging.getLogger('websockets').setLevel(logging.INFO)


def main():
    port = 8765
    event = asyncio.Event()
    
    # Iniciar WebSocket_ActorServer
    server = WebSocket_ActorServer(port=port, host="0.0.0.0", stop_flag=event)
    try:
        asyncio.run(server.serverLoop())
    except KeyboardInterrupt:
        event.set()

if __name__ == "__main__":
    main()
