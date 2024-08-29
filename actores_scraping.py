import asyncio
import aiohttp
from bs4 import BeautifulSoup

async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()

async def parse(url):
    async with aiohttp.ClientSession() as session:
        html = await fetch(session, url)
        soup = BeautifulSoup(html, 'html.parser')
        title = soup.find('title').text
        print(f'Title: {title}')

async def main(urls):
    tasks = [parse(url) for url in urls]
    await asyncio.gather(*tasks)

urls = [
    'https://example.com',
    'https://anotherexample.com'
]

# Ejecuta el bucle de eventos
asyncio.run(main(urls))
