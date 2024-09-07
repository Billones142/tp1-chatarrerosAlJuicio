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
from src import ActorServer as ActorServerPyro5, Comunication_WebSocket_ActorsServer, actors_ServerStart, stop_flag

#jsonPath= '../paginasAScrapear.json'

class TestCommunication(unittest.IsolatedAsyncioTestCase):
  def setUp(self):
    self.port = 8765
    self.stop_flag = threading.Event()  # Usamos un Event en lugar de una bandera booleana
    self.actor_server_thread = threading.Thread(target=actors_ServerStart, args=(self.port, self.stop_flag))
    self.actor_server_thread.daemon = True
    self.actor_server_thread.start()
    time.sleep(2)  # Espera que el servidor arranque

  def tearDown(self):
    self.stop_flag.set()  # Detenemos el servidor
    self.actor_server_thread.join()  # Esperamos a que el hilo termine
    return super().tearDown()

  async def test_comunicacion_WebSocket_(self):
    async with Comunication_WebSocket_ActorsServer(f"ws://localhost:{self.port}") as serverActores:
      response= await serverActores.ask_scrapper_actor("youtube.com") # elegido por su complejidad y longitud
      print("respuesta:",response)
    self.assertGreater(len(response), 300) # simple checkeo para ver que la respuesta es grande


if __name__ == '__main__':
    unittest.main(verbosity=2)