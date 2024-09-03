from jsonParse import parsePaginasJson
from scrappingActor import ScraperActor, ActorRef
from typing import Tuple
import asyncio
import Pyro5

jsonPath= 'paginasAScrapear.json'


async def main():
    urlsToScrape= parsePaginasJson(jsonPath)

    # Lista para almacenar las referencias de los actores
    #actor_refs = list[(ActorRef[ScraperActor],str)]
    actorRefs: list[Tuple[ActorRef[ScraperActor], str]]= []

    # Crear actores para cada tarea de scraping
    for datos in urlsToScrape:
        actor_ref = ScraperActor.start()
        actorRefs.append((actor_ref, datos.url))


    # Ejecutar el scraping y obtener los resultados
    for actorData, url in actorRefs:
        htlmString = actorData.ask({'command': 'scrape', 'url': url})
        print(f"Titles from {url}: {htlmString}")

    # Detener los actores
    for actor_ref, _ in actorRefs:
        actor_ref.stop()

def main2():
    uri = input("Introduce la URI del servidor: ")
    server = Pyro5.api.Proxy(uri)

    url_to_scrape = "http://mercadolibre.com"
    print(f"Enviando solicitud de scraping para {url_to_scrape}...")
    result = server.start_actor(url_to_scrape)
    
    print("Resultados obtenidos:")
    print(result)

if __name__ == '__main__':
    asyncio.run(main= main2())