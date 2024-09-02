import pykka
from pykka import ActorRef
import requests
from bs4 import BeautifulSoup

class ScraperActor(pykka.ThreadingActor):
    def on_receive(self, message):
        command = message.get('command')
        url = message.get('url')

        if command == 'scrape':
            return self.scrapeHtml(url)

    def scrapeHtml(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Ejemplo simple: obtén todos los títulos de la página
            #titles = [title.get_text() for title in soup.find_all('h1')]
            return soup
        except requests.exceptions.RequestException as e:
            return f"Error scraping {url}: {e}"