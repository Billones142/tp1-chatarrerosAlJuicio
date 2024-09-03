import pykka
from bs4 import BeautifulSoup
from typing import List, TypedDict

class LinksAndPrices(TypedDict):
    link: str
    price: str

def parse_MercadoLibre(soup: BeautifulSoup) -> List[LinksAndPrices]:
    precios_y_enlaces= []
    productos = soup.find_all('a', class_='poly-component__title')
    for producto in productos:
        titulo = producto.find('h2', class_='poly-box').text
        if "2060" in titulo:
            precio_tag = producto.find_next('span', class_='andes-money-amount__fraction')
            if precio_tag:
                try:
                    precio = int(precio_tag.text.replace('.', ''))
                    enlace = producto['href']
                    precios_y_enlaces.append(LinksAndPrices(price= precio, link= enlace))
                except ValueError:
                    print(f"Error al procesar el precio en Mercadolibre: {precio_tag.text}")
    return precios_y_enlaces


def parse_Uranostream(soup: BeautifulSoup) -> List[LinksAndPrices]:
    precios_y_enlaces = []
    productos = soup.find_all('a', class_='woocommerce-LoopProduct-link woocommerce-loop-product__link')
    for producto in productos:
        titulo = producto.text
        if "2060" in titulo:
            precio_tag = producto.find_next('span', class_='woocommerce-Price-amount amount')
            if precio_tag:
                try:
                    precio = int(precio_tag.text.replace('$', '').replace('.', '').replace(',', ''))
                    enlace = producto['href']
                    precios_y_enlaces.append(LinksAndPrices(price= precio, link= enlace))
                except ValueError:
                    print(f"Error al procesar el precio en Uranostream: {precio_tag.text}")
    return precios_y_enlaces


def parse_Hardgamers(soup: BeautifulSoup) -> List[LinksAndPrices]:
    precios_y_enlaces = []
    productos = soup.find_all('h3', class_='product-title line-clamp')
    for producto in productos:
        titulo = producto.text.strip()
        if "2060" in titulo:
            precio_container = producto.find_next('div', class_='d-flex')
            if precio_container:
                try:
                    precio_tag = precio_container.find('h2', itemprop='price')
                    if precio_tag:
                        precio_text = precio_tag.text.strip()
                        precio = int(precio_text.replace('.', '').replace(',', ''))
                        enlace = producto.find_parent('a')['href']
                        precios_y_enlaces.append(LinksAndPrices(price= precio, link= enlace))
                except ValueError:
                    print(f"Error al procesar el precio en Hardgamers: {precio_tag.text}")
    return precios_y_enlaces