import json
from web.views import SWAPI_BASE_URL

from django.urls import reverse


def test_index(client, requests_mock):
    url = reverse('index')
    content = json.dumps({})
    requests_mock.register_uri('GET', SWAPI_BASE_URL, text=content)
    response = client.get(url)
    assert response.status_code == 200
