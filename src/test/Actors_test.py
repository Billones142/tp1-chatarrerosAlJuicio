import threading
import unittest
from typing import Tuple
import Pyro5.api
from pykka import ActorRef


# importaciones propias del proyecto
#from ..actors.parse.parseActor import ParseActor
from src.actors import ScraperActor, ParseActor
from src.utils import parsePaginasJson

jsonPath= '../paginasAScrapear.json'

class TestActors(unittest.TestCase): # python -m unittest src.test.scrappingActor_test.TestScrappingActors
    def setUp(self) -> None:
        self.scrapperActor= ScraperActor.start()
        self.parserActor= ParseActor().start()
        return super().setUp()
    
    def tearDown(self) -> None:
        self.scrapperActor.stop()
        self.parserActor.stop()
        return super().tearDown()


    def test_ScrappingActor_scrapeHtml(self):
        # Ejecutar el scraping y obtener los resultados
        actor= ScraperActor.start()
        htlmString = actor.ask({'command': 'scrapeHtml', 'url': "https://youtube.com"})
        actor.stop()

        self.assertNotEqual(htlmString, None, msg= "El html esta vacio")
        self.assertGreater(len(htlmString), 300)

    def test_ParserActor_parseMercadolibre(self):
        htlmString = self.scrapperActor.ask({
                                            'command': 'scrapeHtml',
                                            'url': "https://listado.mercadolibre.com.ar/computacion/perifericos-pc/mouses-teclados/mouses/razer/nuevo/mouse-razer-viper-ultimate_OrderId_PRICE_NoIndex_True#applied_filter_id%3DITEM_CONDITION%26applied_filter_name%3DCondici%C3%B3n%26applied_filter_order%3D4%26applied_value_id%3D2230284%26applied_value_name%3DNuevo%26applied_value_order%3D1%26applied_value_results%3D54%26is_custom%3Dfalse"
                                            })
        parsedQuery = self.parserActor.ask({'command': 'parseMercadoLibre', 'productName': 'Razer', 'htmlString': htlmString})
        
        self.assertIsNotNone(parsedQuery)
        self.assertNotEqual(len(parsedQuery), 0)

    def test_ParserActor_parseUranostream(self):
        htlmString = self.scrapperActor.ask({'command': 'scrapeHtml', 'url': "https://uranostream.com/?s=3050&post_type=product&dgwt_wcas=1"})
        parsedQuery= self.parserActor.ask({'command': 'parseUranostream', 'productName': '3050', 'htmlString': htlmString})

        self.assertIsNotNone(parsedQuery)
        self.assertNotEqual(len(parsedQuery), 0)

    def test_ParserActor_parseUranostream2(self):
        htlmString = self.scrapperActor.ask({'command': 'scrapeHtml', 'url': "https://uranostream.com/?s=4090&post_type=product&dgwt_wcas=1"})
        parsedQuery= self.parserActor.ask({'command': 'parseUranostream', 'productName': '4090', 'htmlString': htlmString})

        self.assertIsNotNone(parsedQuery)
        self.assertNotEqual(len(parsedQuery), 0)

    def test_ParserActor_parse_Hardgamers(self):
        htlmString = self.scrapperActor.ask({'command': 'scrapeHtml', 'url': "https://www.hardgamers.com.ar/search?text=2060"})
        parsedQuery= self.parserActor.ask({'command': 'parseHardgamers', 'productName': '2060', 'htmlString': htlmString})

        self.assertIsNotNone(parsedQuery)
        self.assertNotEqual(len(parsedQuery), 0)

if __name__ == '__main__':
    unittest.main(verbosity=2)