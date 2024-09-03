import pykka
from pykka import ActorRef
import requests
from bs4 import BeautifulSoup

class ScraperActor(pykka.ThreadingActor):
    def on_receive(self, message):
        command = message.get('command')

        if command == 'scrape':
            url = message.get('url')
            return self.scrapeHtml(url)
        elif command == 'parse':
            htmlString = message.get('htmlString')
            return self.scrapeHtml(htmlString)

    def scrapeHtml(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            htmlString = BeautifulSoup(response.content, 'html.parser')
            return htmlString
        except requests.exceptions.RequestException as e:
            return f"Error scraping {url}: {e}"
    
    def parseHtml(self, htlmString):
        return htlmString