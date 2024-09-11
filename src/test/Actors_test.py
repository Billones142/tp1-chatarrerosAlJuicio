import threading
import unittest
from typing import Tuple
import Pyro5.api
from pykka import ActorRef


# importaciones propias del proyecto
#from ..actors.parse.parseActor import ParseActor
from src.actors import ScraperActor
from src.utils import parsePaginasJson

jsonPath= '../paginasAScrapear.json'

class TestActors(unittest.TestCase): # python -m unittest src.test.scrappingActor_test.TestScrappingActors
    def setUp(self) -> None:
        return super().setUp()
    
    def tearDown(self) -> None:
        print(threading.enumerate())
        return super().tearDown()


    def test_ScrappingActor_scrapeHtml(self):
        # Ejecutar el scraping y obtener los resultados
        actor= ScraperActor.start()
        htlmString = actor.ask({'command': 'scrapeHtml', 'url': "https://youtube.com"})
        actor.stop()

        print(htlmString)

        self.assertNotEqual(htlmString, None, msg= "El html esta vacio")
        self.assertGreater(len(htlmString), 300)

    def test_ParserActor_parseMercadolibre(self): # TODO
        # Ejecutar el scraping y obtener los resultados
        actor= ScraperActor.start()
        htlmString = actor.ask({'command': 'scrape', 'url': "https://youtube.com"})
        actor.stop()

    def test_ParserActor_parseUranostream(self): # TODO
        # Ejecutar el scraping y obtener los resultados
        actor= ScraperActor.start()
        htlmString = actor.ask({'command': 'scrape', 'url': "https://youtube.com"})
        actor.stop()

    def test_ParserActor_parse_Hardgamers(self): # TODO
        # Ejecutar el scraping y obtener los resultados
        actor= ScraperActor.start()
        htlmString = actor.ask({'command': 'scrape', 'url': "https://youtube.com"})
        actor.stop()

if __name__ == '__main__':
    unittest.main(verbosity=2)