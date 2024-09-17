import json
import pykka
from bs4 import BeautifulSoup, Tag, ResultSet
import re


class ParseActor(pykka.ThreadingActor):
    def on_receive(self, message: dict):
        command = message.get('command')
        htmlString = message.get('htmlString')
        nombreProducto= message.get('productName')

        if command == 'parseMercadoLibre': # nombreProducto es 'parseMercadoLibre' cuando se llama al actor por el comando. simil para el resto
            return self.parse_MercadoLibre(nombreProducto= nombreProducto ,htmlString= htmlString)
        elif command == 'parseUranostream':
            return self.parse_Uranostream(nombreProducto= nombreProducto ,htmlString= htmlString)
        elif command == 'parseHardgamers':
            return self.parse_Hardgamers(nombreProducto= nombreProducto ,htmlString= htmlString)
        else:
            raise Exception("El comando no es valido")

    def parse_MercadoLibre(self, nombreProducto: str, htmlString: str) -> list[str]:
        soup= BeautifulSoup(htmlString, 'html.parser')
        precios_y_enlaces= list()
        productos = soup.find('ol', class_='ui-search-layout ui-search-layout--stack shops__layout')

        if productos == None:
            productos: ResultSet[Tag]= soup.find_all("li", class_= "ui-search-layout__item")

        for producto in productos:
            if nombreProducto in producto.text:
                precio_tag = producto.find_next('span', class_='andes-money-amount__fraction')
                try:
                    precio = precio_tag.text
                    enlace = producto.find("h2", "poly-box poly-component__title").find('a', __class= "")["href"]
                    precios_y_enlaces.append({"price": precio, "link": enlace})
                except ValueError:
                    print(f"Error al procesar el precio en Mercadolibre: {precio_tag.text}")
        return json.dumps(precios_y_enlaces)

    def parse_Uranostream(self, nombreProducto: str, htmlString: str) -> list[str]: #TODO: corregir funcionamiento
        soup= BeautifulSoup(htmlString,"html.parser")
        precios_y_enlaces = list()
        productos: ResultSet[Tag] = soup.find_all('div', class_='products row row-small large-columns-6 medium-columns-3 small-columns-2 has-equal-box-heights equalize-box')
        for producto in productos:
            titulo_tag: Tag= producto.find(name='p', class_="name product-title woocommerce-loop-product__title").find(name='a', class_="woocommerce-LoopProduct-link woocommerce-loop-product__link")
            titulo: str = titulo_tag.text
            if nombreProducto in titulo:
                precio_tag = producto.find('span', class_='woocommerce-Price-amount amount').find("bdi")
                if precio_tag:
                    try:
                        precio = precio_tag.text
                        enlace = titulo_tag["href"]
                        precios_y_enlaces.append({"price": precio, "link": enlace})
                    except Exception as e:
                        raise Exception(f"Error al procesar el precio en Uranostream: {precio_tag.text}")
        return json.dumps(precios_y_enlaces)

    def parse_Hardgamers(self, nombreProducto: str, htmlString: str) -> list[str]: #TODO: corregir funcionamiento
        soup= BeautifulSoup(htmlString,"html.parser")
        precios_y_enlaces = list()
        productos: ResultSet[Tag] = soup.find_all('section', class_='row white-background')
        for producto in productos:
            titulo = producto.find('h3',class_= "product-title line-clamp").text
            if nombreProducto in titulo:
                precio_tag: Tag= producto.find_all("h2",class_="product-price")[1]
                precio_text = precio_tag.text
                precio = precio_text
                enlace = producto.find("div", class_='product-description padding-top-20').find("a")['href']
                precios_y_enlaces.append({"price": precio, "link": enlace})
        return json.dumps(precios_y_enlaces)