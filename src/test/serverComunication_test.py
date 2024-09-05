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

#import ActorServer
from src import ActorServer

#jsonPath= '../paginasAScrapear.json'

class TestPyro5Communication(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        # Iniciar el servidor de actores y obtener su URI
        self.actor_uri = self.start_actor_server()
        time.sleep(1)
        self.Actors_server= Pyro5.api.Proxy(self.actor_uri)

    def start_actor_server(self):
        daemon = Pyro5.api.Daemon()
        uri = daemon.register(ActorServer)
        
        # Iniciar el request loop en un hilo separado
        self.actor_server_thread = threading.Thread(target=daemon.requestLoop)
        self.actor_server_thread.daemon = True
        self.actor_server_thread.start()
        
        return str(uri)

    async def test_comunicacion_Pyro5_ScrappingActor(self):
        actorsServer = self.Actors_server

        url_to_scrape = "http://mercadolibre.com"
        
        HtmlResult = actorsServer.start_actor_scrapper(url_to_scrape) # usa la funcion start_actor definida en el servidor de actores mediante Pyro5
        

        self.assertNotEqual(HtmlResult, None)

    async def test_comunicacion_Pyro5_ParseActor(self):
        ActorsServer = self.Actors_server

        url_to_scrape = "https://listado.mercadolibre.com.ar/computacion/componentes-pc/placas/placas-video/fabricante-nvidia/nuevo/rtx-2060_NoIndex_True#applied_filter_id%3DITEM_CONDITION%26applied_filter_name%3DCondici%C3%B3n%26applied_filter_order%3D6%26applied_value_id%3D2230284%26applied_value_name%3DNuevo%26applied_value_order%3D1%26applied_value_results%3D47%26is_custom%3Dfalse"
        htmlResult = ActorsServer.start_actor_scrapper(url_to_scrape) # usa la funcion start_actor definida en el servidor de actores mediante Pyro5

        result = ActorsServer.start_actor_HtmlParser("parseMercadoLibre",htmlResult) # usa la funcion start_actor definida en el servidor de actores mediante Pyro5
        
        self.assertNotEqual(result, None)

if __name__ == '__main__':
    unittest.main(verbosity=2)