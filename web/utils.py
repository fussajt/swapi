import json
import requests
from functools import lru_cache

def fetch_data(url):
    """Yield paginated data from api."""
    if url is None:
        return
    resp = requests.get(url)
    res = json.loads(resp.content)
    yield res.get("results")
    yield from fetch_data(res.get("next"))

@lru_cache(maxsize=200)
def map_planet(url):
    """Map homeworld url to planet name."""
    res = requests.get(url)
    data = json.loads(res.content)
    return data["name"]

def process_data(data):
    """Clean fetched data."""
    default = lambda k, d: d[k]
    key_mapping = {
        "name": default,
        "birth_year": default,
        "eye_color": default,
        "skin_color": default,
        "gender": default,
        "homeworld": lambda k, d: map_planet(d[k])
    }
    return [{k: key_mapping[k](k, d) 
             for k in d if k in key_mapping.keys()
            } for d in data]
