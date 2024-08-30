import json
from os import path
from types import SimpleNamespace

jsonPath= 'paginasAScrapear.json'


def parseJson(jsonPath):
  #try:
    with open(path.join(path.dirname(__file__) , jsonPath), 'r') as jsonPaginasAScrappear:
      paginasAScrapear= json.loads(jsonPaginasAScrappear.read(), object_hook=lambda d: SimpleNamespace(**d))
      return paginasAScrapear;
  #except:
  #  return None

print(parseJson(jsonPath))