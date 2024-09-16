import unittest
import threading
import time
import asyncio

import websockets

# importaciones propias del proyecto
from src import API_ActorsServer, WebSocket_ActorServer 




class TestCommunication(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        print(threading.enumerate())
        self.port = 8765
        self.host = "127.0.0.1"
        self.stop_flag = threading.Event()  # Usamos un Event en lugar de una bandera booleana
        self.actor_server_thread = threading.Thread(target=self.startActorServer, args=(self.port, self.stop_flag), name="loop del servidor")
        self.actor_server_thread.daemon = True
        self.actor_server_thread.start()
        time.sleep(2)  # Espera que el servidor arranque

    def startActorServer(self, port: int, stopFlag):
        server = WebSocket_ActorServer(port=port,host= self.host, stop_flag=stopFlag)
        loop = asyncio.new_event_loop()  # Crear un nuevo event loop para este thread
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(server.serverLoop())  # Ejecuta hasta que la stopFlag cambie
        finally:
            loop.close()  # Cerrar el event loop cuando termina

    def tearDown(self):
        self.stop_flag.set()  # Detenemos el servidor
        self.actor_server_thread.join()  # Esperamos a que el hilo termine
        print("Esperando a que se detengan todos los hilos")
        cant= 0
        lista= [hilo for hilo in threading.enumerate() if ((hilo != threading.main_thread()) or ("asyncio_0" == hilo.getName()))]
        while len(lista) > 1:
            print(f"{cant}: hilos restantes:",[hilo for hilo in threading.enumerate() if hilo != threading.main_thread()]) # se imprimen todos los hilos exepto el principal
            cant+= 1
            time.sleep(1)
        return super().tearDown()

    async def test_ActorServerStart(self):
        self.assertTrue(True)
        async with API_ActorsServer(f"ws://localhost:{self.port}") as serverActores:
            await serverActores.ask_scrapper("adsfa")


    async def test_comunicacion_WebSocket(self):
        async with API_ActorsServer(f"ws://localhost:{self.port}") as serverActores:
            response= await serverActores.ask_scrapper("https://youtube.com") # elegido por su complejidad y longitud

        # si la cadena de error no es 0 hubo un error en el servidor y el resultado no es utilizable
        self.assertEqual(len(response["error"]), 0 , msg= "error en el servidor de actores:\n") # + response["error"])
        # checkeo para ver que la respuesta es grande
        self.assertNotEqual(len(response["result"]), 0, msg= "La cadena de html no tiene contenido")
        self.assertGreater(len(response["result"]), 80, msg= "La cadena de html es muy corta\n cadena: ")#+ response["result"])

    async def test_errorComunicacion_WebSocket(self):
        async with API_ActorsServer(f"ws://localhost:{self.port}") as serverActores:
            response= await serverActores.ask_scrapper("youtube.com") # al no especificar el protocolo https se fuerza una falla en el servidor

        self.assertNotEqual(len(response["error"]), 0 , msg= "no hubo error en el servidor de actores")
        
        self.assertEqual(len(response["result"]), 0, msg= "La cadena de html si tiene contenido\n cadena: " + response["result"])

    async def test_PeticionDeListaJson(self):
        async with API_ActorsServer(f"ws://localhost:{self.port}") as serverActores:
            response= await serverActores.ask_scrapper("youtube.com") # al no especificar el protocolo https se fuerza una falla en el servidor

        # si la cadena de error no es 0 hubo un error en el servidor y el resultado no es utilizable
        self.assertNotEqual(len(response["error"]), 0 , msg= "no hubo error en el servidor de actores")
        # simple checkeo para ver que la respuesta es grande
        self.assertEqual(len(response["result"]), 0, msg= "La cadena de html si tiene contenido\n cadena: " + response["result"])


if __name__ == '__main__':
    unittest.main(verbosity=2)