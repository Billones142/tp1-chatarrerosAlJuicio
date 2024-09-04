import unittest
import threading
import time
from typing import Tuple
import Pyro5.api
from pykka import ActorRef


# importaciones propias del proyecto
#from ..actors.parse.parseActor import ParseActor
#from ..actors.scrapping.scrappingActor import ScraperActor
#from ..utils.jsonParse import parsePaginasJson

from ..mainActors import ActorServer
from ..mainActors import main as start_actor_server

#jsonPath= '../paginasAScrapear.json'

class TestPyro5Communication(unittest.TestCase):

    def setUp(self):
        # Iniciar el servidor de actores y obtener su URI
        self.actor_uri = self.start_actor_server()

    def start_actor_server(self):
        daemon = Pyro5.api.Daemon()
        uri = daemon.register(ActorServer)
        
        # Iniciar el request loop en un hilo separado
        self.actor_server_thread = threading.Thread(target=daemon.requestLoop)
        self.actor_server_thread.daemon = True
        self.actor_server_thread.start()
        
        return str(uri)

    def test_comunicacion_Pyro5_ScrappingActor(self):
        ActorsServer = Pyro5.api.Proxy(self.actor_uri)

        url_to_scrape = "http://mercadolibre.com"
        result = ActorsServer.start_actor(url_to_scrape) # usa la funcion start_actor definida en el servidor de actores mediante Pyro5
        
        self.assertNotEqual(result, None)

def start_actor_server():
    daemon = Pyro5.api.Daemon()
    uri = daemon.register(ActorServer)
    daemon.requestLoop()

if __name__ == '__main__':
    unittest.main(verbosity=2)