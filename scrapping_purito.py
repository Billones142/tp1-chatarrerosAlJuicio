import requests
from bs4 import BeautifulSoup

# URL del listado de productos en MercadoLibre
url = 'https://listado.mercadolibre.com.ar/computacion/componentes-pc/placas/placas-video/fabricante-nvidia/nuevo/rtx-2060_NoIndex_True#applied_filter_id%3DITEM_CONDITION%26applied_filter_name%3DCondici%C3%B3n%26applied_filter_order%3D6%26applied_value_id%3D2230284%26applied_value_name%3DNuevo%26applied_value_order%3D1%26applied_value_results%3D47%26is_custom%3Dfalse'

# Hacer la solicitud HTTP a la URL
response = requests.get(url)

# Analizar el contenido HTML usando el parser 'html.parser'
soup = BeautifulSoup(response.text, 'html.parser')

# Encontrar los elementos <a> que contienen los títulos de los productos
productos = soup.find_all('a', class_='poly-component__title')

# Lista para almacenar pares (precio, enlace) de productos que cumplen con el filtro
precios_y_enlaces = []

# Recorrer cada producto encontrado
for producto in productos:
    # Extraer el título
    titulo = producto.find('h2', class_='poly-box').text
    
    # Filtrar por títulos que contengan "2060"
    if "2060" in titulo:
        # Buscar el precio dentro del mismo bloque de producto
        precio_tag = producto.find_next('span', class_='andes-money-amount__fraction')
        if precio_tag:
            # Extraer el precio y convertirlo a un número entero
            precio = int(precio_tag.text.replace('.', ''))
            
            # Extraer el enlace del producto
            enlace = producto['href']
            
            # Agregar el precio y el enlace a la lista
            precios_y_enlaces.append((precio, enlace))

# Mostrar la cantidad de resultados encontrados
print(f'Cantidad de productos encontrados con "2060" en el título: {len(precios_y_enlaces)}')

# Mostrar el menor de todos los precios encontrados y su enlace
if precios_y_enlaces:
    # Encontrar el par (precio, enlace) con el menor precio
    menor_precio, enlace_menor_precio = min(precios_y_enlaces, key=lambda x: x[0])
    print(f'El menor precio encontrado es: ${menor_precio}')
    print(f'Enlace al producto con el menor precio: {enlace_menor_precio}')
else:
    print('No se encontraron productos con "2060" en el título.')
