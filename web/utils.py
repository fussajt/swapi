import dateutil.parser
import json
from functools import lru_cache

import requests


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

def map_date(value):
    """Retrun date from edited date."""
    return dateutil.parser.isoparse(value).strftime("%Y-%m-%d")
    

def process_data(data):
    """Clean fetched data."""
    default = lambda k, d: d[k]
    value_mapping = {
        "name": default,
        "birth_year": default,
        "eye_color": default,
        "skin_color": default,
        "gender": default,
        "homeworld": lambda k, d: map_planet(d[k]),
        "edited": lambda k, d: map_date(d[k])
    }
    key_map = {
        "edited": "date"
    }
    map_key = lambda k: key_map.get(k, k)
    return [{map_key(k): value_mapping[k](k, d) 
             for k in d if k in value_mapping.keys()
            } for d in data]
