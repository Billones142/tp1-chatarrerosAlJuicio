from .jsonParse import parseJson, parsePaginasJson
from .singleton import Singleton
from .urlOrigin import get_origin, get_main_origin

__all__= ["parseJson",
          "parsePaginasJson",
          "Singleton",
          "get_origin"]