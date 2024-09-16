import unittest

from src import utils

jsonPath= '../paginasAScrapear.json'

class TestCommunication(unittest.IsolatedAsyncioTestCase):
    def test_parsePaginasJson(self):
        paginasJson= utils.parsePaginasJson(jsonPath)
        
        self.assertGreaterEqual(len(paginasJson),2)

        for pagina in paginasJson:
            self.assertIsNotNone(pagina.nombre)
            self.assertGreaterEqual(len(pagina.linksDeCompra),1)

    def test_getOrigin(self):
        url= "https://listado.mercadolibre.com.ar/rtx-2070#D[A:rtx%202070]"
        parsedUrl= utils.get_origin(url)

        self.assertNotEqual(url, parsedUrl)
        self.assertEqual("https://listado.mercadolibre.com.ar",parsedUrl)
    
    def test_getMainOrigin(self):
        url= "https://listado.mercadolibre.com.ar/rtx-2070#D[A:rtx%202070]"
        parsedUrl= utils.get_main_origin(url)
        
        self.assertNotEqual(url, parsedUrl)
        self.assertEqual("https://mercadolibre.com.ar",parsedUrl)

if __name__ == '__main__':
    unittest.main(verbosity=2)