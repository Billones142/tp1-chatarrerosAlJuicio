import pykka
import requests
from bs4 import BeautifulSoup


class ScraperActor(pykka.ThreadingActor):
    def on_receive(self, message):
        command = message.get('command')

        if command == 'scrapeHtml':
            url = message.get('url')
            return self.scrapeHtml(url)

    def scrapeHtml(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            htmlString = BeautifulSoup(response.content, 'html.parser')
            return htmlString
        except requests.exceptions.RequestException as e:
            return f"Error scraping {url}: {e}"