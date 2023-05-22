from django.shortcuts import render
from django.views import generic
from web.utils import fetch_data, process_data
from web.models import Collection
import petl
import logging
logger = logging.getLogger("root")

SWAPI_BASE_URL="https://swapi.dev/api"

class IndexView(generic.ListView):
    model = Collection
    context_object_name = "collection_list"
    template_name = "web/index.html"

def detail(request, rows=10):
    context = {}
    path = request.GET['path']
    table = petl.fromcsv(path)
    sink = petl.MemorySource()
    petl.head(table, rows).tohtml(sink, encoding="utf-8", lineterminator=' ')
    context = {"data": sink.getvalue().decode('utf-8') }

    return render(request, "web/detail.html", context=context)

def fetch(request):
    resource = "people"
    collection = Collection()
    file_path = collection.get_new_file_path(resource)
    for data in fetch_data(f"{SWAPI_BASE_URL}/{resource}"):
        processed = process_data(data)
        collection.write_file(processed, file_path)
        collection.save()
    return render(request, "web/index.html", context={"data": "Finish!"})
