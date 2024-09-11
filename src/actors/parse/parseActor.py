import json
import pykka
from bs4 import BeautifulSoup
from typing import TypedDict
import re


class ParseActor(pykka.ThreadingActor):
    def on_receive(self, message: dict):
        command = message.get('command')
        htmlString = message.get('htmlString')
        nombreProducto= message.get('productName')

        if command == 'parseMercadoLibre':
            return self.parse_MercadoLibre(nombreProducto= nombreProducto ,htmlString= htmlString)
        elif command == 'parseUranostream':
            return self.parse_Uranostream(nombreProducto= nombreProducto ,htmlString= htmlString)
        elif command == 'parseHardgamers':
            return self.parse_Hardgamers(nombreProducto= nombreProducto ,htmlString= htmlString)
        else:
            raise Exception("El comando no es valido")

    def stringInt_to_int(self, string: str) -> int :
        return int(re.sub(r'[$.,]', '', string)) # Remplaza los caracteres "$" "." y "," por un espacio vacio y lo convierte en un numero entero

    def parse_MercadoLibre(self, nombreProducto: str, htmlString: str) -> list[str]: # TODO: modificar para que tome un str y no BeatifulSoup
        soup= BeautifulSoup(htmlString)
        precios_y_enlaces= list()
        productos = soup.find_all('a', class_='poly-component__title')
        for producto in productos:
            titulo = producto.find('h2', class_='poly-box').text
            if nombreProducto in titulo:
                precio_tag = producto.find_next('span', class_='andes-money-amount__fraction')
                if precio_tag:
                    try:
                        precio = self.stringInt_to_int(precio_tag)
                        enlace = producto['href']
                        precios_y_enlaces.append({"price": precio, "link": enlace})
                    except ValueError:
                        print(f"Error al procesar el precio en Mercadolibre: {precio_tag.text}")
        return json.dumps(precios_y_enlaces)

    def parse_Uranostream(self, nombreProducto: str, htmlString: str) -> list[str]:
        soup= BeautifulSoup(htmlString)
        precios_y_enlaces = list[str]()
        productos = soup.find_all('a', class_='woocommerce-LoopProduct-link woocommerce-loop-product__link')
        for producto in productos:
            titulo = producto.text
            if nombreProducto in titulo:
                precio_tag = producto.find_next('span', class_='woocommerce-Price-amount amount')
                if precio_tag:
                    try:
                        precio = self.stringInt_to_int(precio_tag)
                        enlace = producto['href']
                        precios_y_enlaces.append({"price": precio, "link": enlace})
                    except ValueError:
                        print(f"Error al procesar el precio en Uranostream: {precio_tag.text}")
        return json.dumps(precios_y_enlaces)

    def parse_Hardgamers(self, nombreProducto: str, htmlString: str) -> list[str]:
        soup= BeautifulSoup(htmlString)
        precios_y_enlaces = list[str]()
        productos = soup.find_all('h3', class_='product-title line-clamp')
        for producto in productos:
            titulo = producto.text.strip()
            if nombreProducto in titulo:
                precio_container = producto.find_next('div', class_='d-flex')
                if precio_container:
                    try:
                        precio_tag = precio_container.find('h2', itemprop='price')
                        if precio_tag:
                            precio_text = precio_tag.text.strip()
                            precio = self.stringInt_to_int(precio_text)
                            enlace = producto.find_parent('a')['href']
                            precios_y_enlaces.append({"price": precio, "link": enlace})
                    except ValueError:
                        print(f"Error al procesar el precio en Hardgamers: {precio_tag.text}")
        return json.dumps(precios_y_enlaces)