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
        soup = BeautifulSoup(htmlString, 'html.parser')
        precios_y_enlaces = list()
    
    # Extraer productos desde el JSON-LD si está disponible
        data_json = soup.find("script", type="application/ld+json")
        if data_json:
            productos_json = json.loads(data_json.string)
            for producto in productos_json["@graph"]:
                if "Product" in producto["@type"]:
                    if nombreProducto.lower() in producto["name"].lower():
                        precio = producto["offers"]["price"]
                        enlace = producto["offers"]["url"]
                        precios_y_enlaces.append({"price": precio, "link": enlace})
        
        # Si no se encuentran productos en JSON, intentar buscarlos en el HTML
        if not precios_y_enlaces:
            productos = soup.find('ol', class_='ui-search-layout ui-search-layout--stack shops__layout')
            if productos is None:
                productos = soup.find_all("li", class_="ui-search-layout__item")
            
            for producto in productos:
                try:
                    titulo= producto.text.casefold()
                    if (nombreProducto.casefold() in titulo) and (" para " not in titulo):
                        precio_tag = producto.find_next('span', class_='andes-money-amount__fraction')
                        try:
                            precio = precio_tag.text
                            enlace = producto.find("h2", "poly-box poly-component__title").find('a', class_="")["href"]
                            precios_y_enlaces.append({"price": precio, "link": enlace})
                        except (AttributeError, ValueError):
                            print(f"Error al procesar el precio o enlace en Mercadolibre.")
                except (AttributeError, ValueError):
                    print(f"Error al procesar el producto en Mercadolibre.")
        
        return json.dumps(precios_y_enlaces)


    def parse_Uranostream(self, nombreProducto: str, htmlString: str) -> list[str]: #TODO: corregir funcionamiento
        soup= BeautifulSoup(htmlString,"html.parser")
        precios_y_enlaces = list()
        productos: ResultSet[Tag] = soup.find_all('div', class_='products row row-small large-columns-6 medium-columns-3 small-columns-2 has-equal-box-heights equalize-box')
        for producto in productos:
                titulo_tag: Tag= producto.find(name='p', class_="name product-title woocommerce-loop-product__title").find(name='a', class_="woocommerce-LoopProduct-link woocommerce-loop-product__link")
                titulo: str = titulo_tag.text.casefold()
                if (nombreProducto.casefold() in titulo) and (" para " not in titulo):
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
        productos: ResultSet[Tag] = soup.find_all('div', class_='product-description padding-top-20')
        for producto in productos:
            titulo_tag = producto.find('h3',class_= "product-title line-clamp")
            if isinstance(titulo_tag, Tag):
                titulo= titulo_tag.text.casefold()
                if (nombreProducto.casefold() in titulo) and (" para " not in titulo):
                    precio_tag: Tag= producto.find_all("h2",class_="product-price")[1]
                    if precio_tag == None:
                        precio= "0"
                    else:
                        precio = precio_tag.text
                    enlace = producto.find("a", class_="")['href']
                    precios_y_enlaces.append({"price": precio, "link": enlace})
        return json.dumps(precios_y_enlaces)