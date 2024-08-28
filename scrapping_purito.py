import requests
from bs4 import BeautifulSoup

# URL que vamos a scrapear
url = 'https://listado.mercadolibre.com.ar/rtx-2060-asus-dual'

# Realizamos la solicitud a la página
response = requests.get(url)
response.raise_for_status()  # Verifica si la solicitud fue exitosa

# Parseamos el contenido HTML
soup = BeautifulSoup(response.text, 'html.parser')

# Encontramos todos los títulos de los productos
titles = soup.find_all('h2', class_='ui-search-item__title')

# Imprimimos los títulos
for title in titles:
    print(title.text)