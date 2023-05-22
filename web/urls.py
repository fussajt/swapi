from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path(r"api/?P<path>/", views.api, name="api")
]
