import traceback
from websockets.asyncio.server import serve, ServerConnection
import asyncio
import json
import logging


from src.actors import ScraperActor, ParseActor

nombreLogger= "WebSocket_ActorServer"

# Configura el logger del módulo
logger = logging.getLogger(nombreLogger)  # Nombre del logger igual al nombre del módulo
logger.setLevel(logging.DEBUG)  # Establece el nivel de logging

# Configurar el formato de los mensajes de log
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Crear y agregar un manejador para la consola
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

# Crear manejador de archivo
file_handler = logging.FileHandler(f'{nombreLogger.replace(" ","_")}.log')
file_handler.setFormatter(formatter)

# Añadir el manejador al logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)

class WebSocket_ActorServer(): #perdon gaby, es mas facil cuando es una clase
    def __init__(self, port: int, host: str= "localhost", stop_flag: asyncio.Event= asyncio.Event()):
        self.host= host
        self.port= port
        self.stop_flag= stop_flag

    async def startServer(self):
        try:
            self.websocketServer= await serve(handler= self.handle_client, host= self.host, port= self.port, max_size=10 * 1024 * 1024)
        except Exception as e:
            self.scrapperActor.stop(block= True)
            self.parseActor.stop(block= True)
            logging.error("Error al iniciar websocket" + e)
            raise Exception("Error al iniciar websocket:\n" + e)
    
    async def stopServerServices(self):
        logger.info("Stopping server services")
        self.websocketServer.close()
        await self.websocketServer.wait_closed()
        self.scrapperActor.stop(block= True)
        self.parseActor.stop(block= True)
        logger.info("Server services stop successfull")

    async def handle_client(self,websocket: ServerConnection):
        logger.info("New client connected to server: %s", websocket.id)
        async for message in websocket:
            response= await self.handle_message(message) # responde el mensaje
            await websocket.send(response) # envia la respuesta

    async def handle_message(self,message):
        logger.info("Hanlding message")
        response= ""
        error= ""

        try:
            messages = json.loads(message)

            if messages["commandWebSocket"] == "scrapeHtml":
                response= self.ask_scrapper(url= messages["url"])
            elif messages["commandWebSocket"] == "parseHtml":
                response= json.dumps(self.ask_HtmlParser(messages["command"], messages["htmlString"], messages["productName"]))

        except Exception as e:
            logger.error("Error while responding message")
            response= ""
            # Get the last frame from the stack trace
            stack = traceback.extract_tb(e.__traceback__)
            last_frame = stack[-1]
            function_name = last_frame.name
            filename = last_frame.filename
            line_number = last_frame.lineno
            error= f"\nInicio error del servidor ({function_name} en {filename} linea {line_number}):\n" + str(e) + "\n Fin de error del servidor"

        logger.debug("Sending to client: %s",response)
        logger.info("Ended Hanlding message")
        return json.dumps({"error": error,"result":response})

    def ask_scrapper(self,url: str) -> str:
        scrapperActor= ScraperActor.start()
        result= scrapperActor.ask(block= True, message={'command': 'scrapeHtml', 'url': url})
        scrapperActor.stop()
        return result

    def ask_HtmlParser(self, comand: str, htmlString: str, productName: str) -> list:
        parseActor= ParseActor.start()
        result= parseActor.ask(block= True, message={'command': comand, 'htmlString': htmlString, "productName": productName})
        parseActor.stop()
        return result

    async def serverLoop(self):
        await self.startServer()
        while not self.stop_flag.is_set():
            await asyncio.sleep(1)
        logger.info("Shutting down actors websocket server")
        await self.stopServerServices()