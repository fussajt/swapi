from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django.views import generic
from web.utils import fetch_data, process_data
from web.models import Collection
import petl

SWAPI_BASE_URL="https://swapi.dev/api"

class IndexView(generic.ListView):
    """Index page with list of saved collections."""
    model = Collection
    context_object_name = "collection_list"
    template_name = "web/index.html"

def detail(request):
    """Saved collection contents view."""
    context = {}
    path = request.GET['path']
    rows = int(request.GET.get('rows', 10))
    table = petl.fromcsv(path)
    sink = petl.MemorySource()
    petl.head(table, rows).tohtml(sink, encoding="utf-8", lineterminator=' ')
    context = {
        "data": sink.getvalue().decode('utf-8'), 
        "header_list": petl.header(table),
        "rows": rows,
        "path": path
    }
    return render(request, "web/detail.html", context=context)

def fetch(request):
    """Fetch fresh collection."""
    resource = "people"
    collection = Collection()
    file_path = collection.get_new_file_path(resource)
    for data in fetch_data(f"{SWAPI_BASE_URL}/{resource}"):
        processed = process_data(data)
        collection.write_file(processed, file_path)
        collection.save()
    return HttpResponseRedirect(reverse("index"))

def count(request):
    """Aggregate collection view."""
    headers = request.POST.getlist("header")
    path = request.POST["path"]
    table = petl.fromcsv(path)
    sink = petl.MemorySource()
    petl.aggregate(
        table, 
        key=headers, 
        aggregation=len, 
        value=headers[0]
    ).tohtml(sink, encoding="utf-8", lineterminator=' ')
    context = {
        "data": sink.getvalue().decode('utf-8')
    }
    return render(request, "web/count.html", context=context)
