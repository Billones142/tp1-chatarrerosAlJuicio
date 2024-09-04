import pykka
from bs4 import BeautifulSoup
from typing import List, TypedDict
import re


class ParseActor(pykka.ThreadingActor):
  def on_receive(self, message):
    command = message.get('command')
    htmlString = message.get('htmlString')

    if command == 'parseMercadoLibre':
      return self.parse_MercadoLibre(htmlString)
    elif command == 'parseUranostream':
      self.parse_Uranostream(htmlString)
    elif command == 'parseHardgamers':
      self.parse_Hardgamers(htmlString)

  class LinksAndPrices(TypedDict):
    link: str
    price: str
  
  def stringInt_to_int(self, string: str) -> int :
    return int(re.sub(r'[$.,]', '', string)) # Remplaza los caracteres "$" "." y "," por un espacio vacio y lo convierte en un numero entero
  
  """
  class HTML_Element(TypedDict):
    header: str
    class_: str
  

  def soupPriceParse(self, 
  soup : BeautifulSoup,
  *,
  productName: str ,
  sourceName: str,
  productElement: HTML_Element,
  titleElement: HTML_Element,
  priceTagElement: HTML_Element
  ) -> List[LinksAndPrices]:
    productos= soup.find_all(productElement.header, class_= productElement.class_)
    precios_y_enlaces= List[self.LinksAndPrices]()
    for producto in productos:
        titulo = producto.find(titleElement.header, class_= titleElement.class_).text
        if productName in titulo:
            precio_tag = producto.find_next(priceTagElement.header, class_=priceTagElement.class_)
            if precio_tag:
                try:
                    precio = self.stringInt_to_int(precio_tag)
                    enlace = producto['href']
                    precios_y_enlaces.append(self.LinksAndPrices(price= precio, link= enlace))
                except ValueError:
                    print(f"Error al procesar el precio {("en " + sourceName) if sourceName else ''}: {precio_tag.text}")
    return precios_y_enlaces
  """
  
  def parse_MercadoLibre(self, soup: BeautifulSoup) -> List[LinksAndPrices]:
    """
    return self.soupPriceParse(
    soup,
    productName= "2060",
    sourceName= "MercadoLibre",
    productElement= self.HTML_Element(header= 'a', class_= 'poly-component__title'),
    tittleElement= self.HTML_Element(header= 'h2', class_= 'poly-component__title'),
    priceTagElement= self.HTML_Element(header= 'span', class_= 'andes-money-amount__fraction')
    )
    """

    precios_y_enlaces= List[self.LinksAndPrices]()
    productos = soup.find_all('a', class_='poly-component__title')
    for producto in productos:
        titulo = producto.find('h2', class_='poly-box').text
        if "2060" in titulo:
            precio_tag = producto.find_next('span', class_='andes-money-amount__fraction')
            if precio_tag:
                try:
                    precio = self.stringInt_to_int(precio_tag)
                    enlace = producto['href']
                    precios_y_enlaces.append(self.LinksAndPrices(price= precio, link= enlace))
                except ValueError:
                    print(f"Error al procesar el precio en Mercadolibre: {precio_tag.text}")
    return precios_y_enlaces
  
  def parse_Uranostream(self, soup: BeautifulSoup) -> List[LinksAndPrices]:
    precios_y_enlaces = List[self.LinksAndPrices]()
    productos = soup.find_all('a', class_='woocommerce-LoopProduct-link woocommerce-loop-product__link')
    for producto in productos:
        titulo = producto.text
        if "2060" in titulo:
            precio_tag = producto.find_next('span', class_='woocommerce-Price-amount amount')
            if precio_tag:
                try:
                    precio = self.stringInt_to_int(precio_tag)
                    enlace = producto['href']
                    precios_y_enlaces.append(self.LinksAndPrices(price= precio, link= enlace))
                except ValueError:
                    print(f"Error al procesar el precio en Uranostream: {precio_tag.text}")
    return precios_y_enlaces
  
  def parse_Hardgamers(self, soup: BeautifulSoup) -> List[LinksAndPrices]:
    precios_y_enlaces = List[self.LinksAndPrices]()
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
                        precio = self.stringInt_to_int(precio_text)
                        enlace = producto.find_parent('a')['href']
                        precios_y_enlaces.append(self.LinksAndPrices(price= precio, link= enlace))
                except ValueError:
                    print(f"Error al procesar el precio en Hardgamers: {precio_tag.text}")
    return precios_y_enlaces