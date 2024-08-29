import requests
from bs4 import BeautifulSoup

# URL que vamos a scrapear
url = 'https://listado.mercadolibre.com.ar/rtx-2060-asus-dual'
# Hacer la solicitud HTTP a la URL
response = requests.get(url)
# Verifica si la solicitud fue exitosa
response.raise_for_status()
# Analizar el contenido HTML
soup = BeautifulSoup(response.text, 'lxml')

# Encontrar los elementos que contienen los precios
precios = soup.find_all('span', class_='andes-money-amount__fraction')

# Mostrar los precios de los productos
for precio in precios:
    print(int(precio.text.replace('.','')))