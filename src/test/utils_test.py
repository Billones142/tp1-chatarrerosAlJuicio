import unittest

from src import utils

jsonPath= '../paginasAScrapear.json'

class TestCommunication(unittest.IsolatedAsyncioTestCase): # TODO
    def test(self):
        utils.parsePaginasJson(jsonPath)

if __name__ == '__main__':
    unittest.main(verbosity=2)