import json

from django.urls import reverse

from web.models import Collection
from web.utils import map_planet, process_data, map_date
from web.views import SWAPI_BASE_URL


def test_fetch(db, client, requests_mock):
    """Test fetch view. It results in creation of new Collection record
    and redirection to Index page.
    """
    url = reverse('fetch')
    content = json.dumps({
        "count": 1,
        "next": None,
        "results": [{"name": "R2-D2"}]
    })
    requests_mock.register_uri('GET', f"{SWAPI_BASE_URL}/people", text=content)
    response = client.get(url)
    assert response.status_code == 302
    assert response.url == "/"
    assert Collection.objects.all().count() == 1

def test_cache(requests_mock):
    """Test if calls to plantes resource is cached."""
    url_one = "https://swapi.dev/api/planets/1/"
    url_two = "https://swapi.dev/api/planets/2/"
    content_one = json.dumps({"name": "Tatooine"})
    content_two = json.dumps({"name": "Naboo"})
    requests_mock.register_uri('GET', url_one, text=content_one)
    requests_mock.register_uri('GET', url_two, text=content_two)
    data = [
        {"name": "R2-D2", "homeworld": url_one},
        {"name": "C-3PO", "homeworld": url_two},
        {"name": "Skywalker", "homeworld": url_two},
        {"name": "Leia", "homeworld": url_two}
    ]
    process_data(data)
    assert map_planet.cache_info().hits == 2

def test_date_parser():
    """Test if edited date is parsed properly."""
    iso_date = "2014-12-10T16:44:31.486000Z"
    assert map_date(iso_date) == "2014-12-10"

def test_key_mapping():
    """Test if edited key is mapped to date key."""
    input = [
        {"edited":  "2014-12-10T16:44:31.486000Z"}
    ]
    output = process_data(input)
    assert "date" in output[0]
    assert output[0]["date"] == "2014-12-10"
