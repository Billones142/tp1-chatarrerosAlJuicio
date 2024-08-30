import pykka
import requests
from bs4 import BeautifulSoup

class ScraperActor(pykka.ThreadingActor):
    def scrape(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            # Ejemplo simple: obtén todos los títulos de la página
            titles = [title.get_text() for title in soup.find_all('h1')]
            return titles
        except requests.exceptions.RequestException as e:
            return f"Error scraping {url}: {e}"

# URLs que queremos scrapear
urls = [
    'https://mercadolibre.com',
    'https://compragamer.com',
    # Agrega más URLs según sea necesario
]

# Lista para almacenar las referencias de los actores
actor_refs = []

# Crear actores para cada tarea de scraping
for url in urls:
    actor_ref = ScraperActor.start()
    actor_refs.append((actor_ref, url))

# Ejecutar el scraping y obtener los resultados
for actor_ref, url in actor_refs:
    future = actor_ref.ask({'command': 'scrape', 'url': url})
    titles = future.get()
    print(f"Titles from {url}: {titles}")

# Detener los actores
for actor_ref, _ in actor_refs:
    actor_ref.stop()