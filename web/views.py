from django.shortcuts import render
from web.utils import fetch_data, process_data
from web.models import Collection
from tempfile import TemporaryFile
import requests
import json

SWAPI_BASE_URL="https://swapi.dev/api"

def index(request):
    return render(request, "web/index.html")

def fetch(request):
    resource = "people"
    collection = Collection()
    file_path = collection.get_new_file_path(resource)
    for data in fetch_data(f"{SWAPI_BASE_URL}/{resource}"):
        processed = process_data(data)
        collection.write_file(processed, file_path)
        collection.save()
    return render(request, "web/index.html", context={"data": "Finish!"})
