import requests
from bs4 import BeautifulSoup

# URL de las diferentes páginas que vamos a scrapear
urls = [
    'https://listado.mercadolibre.com.ar/computacion/componentes-pc/placas/placas-video/fabricante-nvidia/nuevo/rtx-2060_NoIndex_True#applied_filter_id%3DITEM_CONDITION%26applied_filter_name%3DCondici%C3%B3n%26applied_filter_order%3D6%26applied_value_id%3D2230284%26applied_value_name%3DNuevo%26applied_value_order%3D1%26applied_value_results%3D47%26is_custom%3Dfalse',
    'https://uranostream.com/categoria-producto/componentes/placa-de-video/',
    'https://www.hardgamers.com.ar/search?text=2060'
]

def scrapeando_mercadolibre(url):
    precios_y_enlaces = []
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    productos = soup.find_all('a', class_='poly-component__title')
    for producto in productos:
        titulo = producto.find('h2', class_='poly-box').text
        if "2060" in titulo:
            precio_tag = producto.find_next('span', class_='andes-money-amount__fraction')
            if precio_tag:
                try:
                    precio = int(precio_tag.text.replace('.', ''))
                    enlace = producto['href']
                    precios_y_enlaces.append((precio, enlace))
                except ValueError:
                    print(f"Error al procesar el precio en Mercadolibre: {precio_tag.text}")
    return precios_y_enlaces

def scrapeando_uranostream(url):
    precios_y_enlaces = []
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    productos = soup.find_all('a', class_='woocommerce-LoopProduct-link woocommerce-loop-product__link')
    for producto in productos:
        titulo = producto.text
        if "2060" in titulo:
            precio_tag = producto.find_next('span', class_='woocommerce-Price-amount amount')
            if precio_tag:
                try:
                    precio = int(precio_tag.text.replace('$', '').replace('.', '').replace(',', ''))
                    enlace = producto['href']
                    precios_y_enlaces.append((precio, enlace))
                except ValueError:
                    print(f"Error al procesar el precio en Uranostream: {precio_tag.text}")
    return precios_y_enlaces

def scrapeando_hardgamers(url):
    precios_y_enlaces = []
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
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
                        precios_y_enlaces.append((precio, enlace))
                except ValueError:
                    print(f"Error al procesar el precio en Hardgamers: {precio_tag.text}")
    return precios_y_enlaces

def main():
    menor_precio_global = float('inf')
    enlace_menor_precio_global = None

    for url in urls:
        if 'mercadolibre' in url:
            precios_y_enlaces = scrapeando_mercadolibre(url)
        elif 'uranostream' in url:
            precios_y_enlaces = scrapeando_uranostream(url)
        elif 'hardgamers' in url:
            precios_y_enlaces = scrapeando_hardgamers(url)
        else:
            print(f"No se encontró función de scraping para la URL: {url}")
            continue

        # Mostrar la cantidad de resultados encontrados
        print(f'\nURL: {url}')
        print(f'Cantidad de productos encontrados con "2060" en el título: {len(precios_y_enlaces)}')

        # Mostrar el menor de todos los precios encontrados y su enlace
        if precios_y_enlaces:
            menor_precio, enlace_menor_precio = min(precios_y_enlaces, key=lambda x: x[0])
            print(f'El menor precio encontrado es: ${menor_precio}')
            print(f'Enlace al producto con el menor precio: {enlace_menor_precio}')
            
            # Comparar con el menor precio global
            if menor_precio < menor_precio_global:
                menor_precio_global = menor_precio
                enlace_menor_precio_global = enlace_menor_precio
        else:
            print('No se encontraron productos con "2060" en el título.')

    # Mostrar el menor precio global y su enlace
    if enlace_menor_precio_global:
        print(f'\nEl menor precio global encontrado es: ${menor_precio_global}')
        print(f'Enlace al producto con el menor precio global: {enlace_menor_precio_global}')
    else:
        print('No se encontraron productos con "2060" en el título en ninguna URL.')

# Ejecutar la función principal
main()
