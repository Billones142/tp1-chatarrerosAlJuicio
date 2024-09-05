import Pyro5.api
from .src.actors.scrapping.scrappingActor import ScraperActor
from .src.actorServerClass import start_server


def main():
    daemon, uri = start_server()
    
    print(f"La URI del servidor es: {str(uri)}")
    daemon.requestLoop()

if __name__ == "__main__":
    main()