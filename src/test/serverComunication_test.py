import unittest
import threading
import time
import asyncio

import websockets

# importaciones propias del proyecto
from src.websocket import API_ActorsServer, WebSocket_ActorServer, ErrorActoresAPI 




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
        error= False
        async with API_ActorsServer(f"ws://localhost:{self.port}") as serverActores:
            try:
                await serverActores.ask_scrapper("adsfa")
            except ErrorActoresAPI:
                error= True
            self.assertTrue(error)



    async def test_comunicacion_WebSocket(self):
        async with API_ActorsServer(f"ws://localhost:{self.port}") as serverActores:
            try:
                response= await serverActores.ask_scrapper("https://youtube.com") # elegido por su complejidad y longitud
            except ErrorActoresAPI:
                self.assertTrue(False, msg= "error en el servidor de actores:\n") # + response["error"])

        # si la cadena de error no es 0 hubo un error en el servidor y el resultado no es utilizable
        
        # checkeo para ver que la respuesta es grande
        self.assertNotEqual(len(response), 0, msg= "La cadena de html no tiene contenido")
        self.assertGreater(len(response), 80, msg= "La cadena de html es muy corta")

    async def test_errorComunicacion_WebSocket(self):
        async with API_ActorsServer(f"ws://localhost:{self.port}") as serverActores:
            try:
                response= await serverActores.ask_scrapper("youtube.com") # al no especificar el protocolo https se fuerza una falla en el servidor
                self.assertTrue(False , msg= "no hubo error en el servidor de actores") # si se llega aqui significa que no hubo error
            except Exception:
                self.assertTrue(True)


    async def test_PeticionDeListaJson(self): # TODO: agregar mas verificaciones
        async with API_ActorsServer(f"ws://localhost:{self.port}") as serverActores:
            htmlResponse= await serverActores.ask_scrapper("https://listado.mercadolibre.com.ar/2060#D[A:2060]") # al no especificar el protocolo https se fuerza una falla en el servidor
            pasedHtml= await serverActores.ask_parser(command="parseMercadoLibre", htmlString= htmlResponse, productName= "2060")


        self.assertGreaterEqual(len(pasedHtml),1)

    async def test_PeticionDeListaJson2(self): # TODO: agregar mas verificaciones
        async with API_ActorsServer(f"ws://localhost:{self.port}") as serverActores:
            htmlResponse= await serverActores.ask_scrapper("https://listado.mercadolibre.com.ar/2060#D[A:2060]") # al no especificar el protocolo https se fuerza una falla en el servidor
            pasedHtml= await serverActores.ask_parser(command="parseUranostream", htmlString= htmlResponse, productName= "2060")


        self.assertGreaterEqual(len(pasedHtml),1)


if __name__ == '__main__':
    unittest.main(verbosity=2)