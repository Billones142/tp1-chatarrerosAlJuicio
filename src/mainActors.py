import Pyro5.api
from scrappingActor import ScraperActor

@Pyro5.api.expose
class ActorServer:
    def start_actor(self, url):
        actor_ref = ScraperActor.start()
        result = actor_ref.proxy().scrape(url)
        actor_ref.stop()
        return result

def main():
    # Iniciar el servidor Pyro5
    daemon = Pyro5.api.Daemon()  # Crear el Daemon de Pyro5
    uri = daemon.register(ActorServer)  # Registrar el objeto en el daemon
    
    print(f"Servidor disponible en {uri}")
    daemon.requestLoop()  # Iniciar el bucle de solicitudes

if __name__ == "__main__":
    main()
