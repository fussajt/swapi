import json
import requests
import logging
from functools import lru_cache

logger = logging.getLogger("root")

def fetch_data(url):
    if url is None:
        return
    resp = requests.get(url)
    res = json.loads(resp.content)
    yield res.get("results")
    yield from fetch_data(res.get("next"))

@lru_cache(maxsize=200)
def map_planet(url):
    res = requests.get(url)
    data = json.loads(res.content)
    return data["name"]

def process_data(data):
    key_mapping = {
        "name": lambda k, d: d[k],
        "birth_year": lambda k, d: d[k],
        "homeworld": lambda k, d: map_planet(d[k])
    }
    return [{k: key_mapping[k](k, d) 
             for k in d if k in key_mapping.keys()
            } for d in data]
