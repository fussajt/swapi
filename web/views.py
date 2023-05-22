from django.shortcuts import render
import requests
import json

SWAPI_BASE_URL="https://swapi.dev/api/"

def index(request):
    res = requests.get(SWAPI_BASE_URL)
    data = json.loads(res.content)
    return render(request, "web/index.html", context={"data": data})

def api(request, path):
    res = requests.get(f"{SWAPI_BASE_URL}/{path}")
    data = json.loads(res.content)
    return render(request, "web/detail.html", context={"data": data})
