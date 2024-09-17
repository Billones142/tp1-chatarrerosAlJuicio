from .jsonParse import parseJson, parsePaginasJson
from .singleton import Singleton
from .urlOrigin import get_origin, get_main_origin
from .encontrarElProductoMasBarato import limpiar_precio, encontrar_producto_mas_barato

__all__= ["parseJson",
          "parsePaginasJson",
          "Singleton",
          "get_origin",
          "limpiar_precio",
          "encontrar_producto_mas_barato",
          "get_main_origin"
          ]