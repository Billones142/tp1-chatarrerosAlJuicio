import unittest
from typing import Tuple
import Pyro5.api
# importaciones propias del proyecto
from actors.scrappingActor import ScraperActor, ActorRef
from utils.jsonParse import parsePaginasJson

jsonPath= 'paginasAScrapear.json'

class TestStringMethods(unittest.TestCase):

    def test_ScrappingActor_scrapeHtml(self):
        urlsToScrape= parsePaginasJson(jsonPath)

        # Lista para almacenar las referencias de los actores
        actorRefs: list[ Tuple[ ActorRef[ScraperActor] , str ] ]= []

        # Crear actores para cada tarea de scraping
        for datos in urlsToScrape:
            actor_ref = ScraperActor.start()
            actorRefs.append((actor_ref, datos.url))


        # Ejecutar el scraping y obtener los resultados
        htmlList= []
        for actorData, url in actorRefs:
            htlmString = actorData.ask({'command': 'scrape', 'url': url})
            htmlList.append(htlmString)

        # Detener los actores
        for actor_ref, _ in actorRefs:
            actor_ref.stop()
        self.assertNotEqual(htlmString, None)
    
    def test_Pyro5_ScrappingActor():
        uri = input("Introduce la URI del servidor: ")
        server = Pyro5.api.Proxy(uri)

        url_to_scrape = "http://mercadolibre.com"
        print(f"Enviando solicitud de scraping para {url_to_scrape}...")
        result = server.start_actor(url_to_scrape)
        
        print("Resultados obtenidos:")
        print(result)

    """ ejemplos
    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)
    """

if __name__ == '__main__':
    unittest.main(verbosity=2)