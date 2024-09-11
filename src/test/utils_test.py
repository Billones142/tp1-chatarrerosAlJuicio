import unittest

from src.utils import parseJson, parsePaginasJson

jsonPath= '../paginasAScrapear.json'

class TestCommunication(unittest.IsolatedAsyncioTestCase): # TODO
    def test(self):
        parsePaginasJson(jsonPath)

if __name__ == '__main__':
    unittest.main(verbosity=2)