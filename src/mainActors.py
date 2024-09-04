import Pyro5.api
from actors.scrapping.scrappingActor import ScraperActor

@Pyro5.api.expose
class ActorServer:
    def start_actor(self, url):
        actor_ref = ScraperActor.start()
        result = actor_ref.proxy().scrapeHtml(url)
        actor_ref.stop()
        return result

def start_server():
    # Iniciar el servidor Pyro5
    daemon = Pyro5.api.Daemon()  # Crear el Daemon de Pyro5
    actor_server = ActorServer()
    uri = daemon.register(actor_server)  # Registrar el objeto en el daemon
    
    return daemon, uri

def main():
    daemon, uri = start_server()
    
    print(f"La URI del servidor es: {str(uri)}")
    daemon.requestLoop()

if __name__ == "__main__":
    main()