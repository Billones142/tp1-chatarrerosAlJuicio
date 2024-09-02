from jsonParse import parsePaginasJson
from scrappingActor import ScraperActor, ActorRef
from typing import Tuple
import asyncio

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

if __name__ == '__main__':
    asyncio.run(main= main())