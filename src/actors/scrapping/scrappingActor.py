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
        response = requests.get(url)
        response.raise_for_status() # no se manejan los errores desde aca
        htmlString = str(BeautifulSoup(response.content, 'html.parser'))
        return htmlString