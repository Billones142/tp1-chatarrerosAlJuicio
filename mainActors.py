#import Pyro5.api
#from .src.actors.scrapping.scrappingActor import ScraperActor
#from .src.actorServerClass import start_server
import asyncio
from websocket.websocket_actors import serverStart as actorsServerStart, serverLoop

"""
def main():
    daemon, uri = start_server()
    
    print(f"La URI del servidor es: {str(uri)}")
    daemon.requestLoop()
"""

# Iniciar el servidor WebSocket
def main():
    asyncio.run(serverLoop(port= 8765))

if __name__ == "__main__":
    main()