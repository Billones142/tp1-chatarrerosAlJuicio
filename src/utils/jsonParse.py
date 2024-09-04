import json
from os import path
from typing import List

class Pagina:
  nombre: str
  valor: int
  linksDeCompra: List[str]

  def __init__(self, nombre, linksDeCompra):
    self.nombre = nombre
    self.linksDeCompra= linksDeCompra

  def __repr__(self): 
    return f"Pagina(nombre={self.nombre!r}, valor={self.valor!r})"

  def __str__(self):
    return f"Pagina: {self.nombre}, Valor: {self.valor}"

def parseJson(jsonPath: str, ClassType: type) -> list | object:
  try:
    # Abre el archivo JSON para leer
    with open(path.join(path.dirname(__file__), jsonPath), 'r') as json_file:
      # Carga el contenido del archivo JSON en un diccionario
      data = json.load(json_file)
      # Verifica si el JSON es una lista o un solo objeto
      if isinstance(data, List):
        # Si es una lista, crea una instancia para cada elemento
        return [ClassType(**item) for item in data]
      else:
        # Si es un solo objeto, crea una instancia directamente
        return ClassType(**data)
  except FileNotFoundError:
      print(f"Error: El archivo '{jsonPath}' no se encontró.")
  except json.JSONDecodeError:
      print(f"Error: El archivo '{jsonPath}' no contiene un JSON válido.")
  except Exception as e:
      print(f"Error inesperado: {e}")

def parsePaginasJson(jsonPath: str) -> list[Pagina]:
  return parseJson(jsonPath, Pagina)

# Ejemplo de uso:
# Supongamos que el archivo JSON es algo como:
# {
#   "nombre": "Página 1",
#   "valor": 42
# }

# O para un JSON de lista:
# [
#   {"nombre": "Página 1", "valor": 42},
#   {"nombre": "Página 2", "valor": 84}
# ]