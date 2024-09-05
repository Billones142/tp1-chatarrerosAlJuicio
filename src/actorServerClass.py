from .actors.scrapping.scrappingActor import ScraperActor
from .actors.parse.parseActor import ParseActor
import Pyro5.api
import logging
logging.basicConfig(level=logging.DEBUG)

@Pyro5.api.expose
class ActorServer:
    def start_actor_scrapper(self, url: str):
        try:
            actor_ref = ScraperActor.start()
            result = actor_ref.ask({'command': 'scrapeHtml', 'url': url})
            actor_ref.stop()
            return str(result)
        except Exception as e:
            logging.exception("Error en start_actor_scrapper")
            raise  # Vuelve a lanzar la excepción para que el cliente pueda capturarla
    
    def start_actor_HtmlParser(self, comand: str, htmlString: str):
        try:
            actor_ref = ParseActor.start()
            result = actor_ref.ask({'command': comand, 'htmlString': htmlString})
            actor_ref.stop()
            return result
        except Exception as e:
            logging.exception("Error en start_actor_HtmlParser")
            raise  # Vuelve a lanzar la excepción para que el cliente pueda capturarla

def start_server():
    # Iniciar el servidor Pyro5
    daemon = Pyro5.api.Daemon()  # Crear el Daemon de Pyro5
    actor_server = ActorServer()
    uri = daemon.register(actor_server)  # Registrar el objeto en el daemon
    
    return daemon, uri