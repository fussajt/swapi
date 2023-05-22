from django.urls import path

from . import views

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("detail", views.detail, name="detail"),
    path("fetch", views.fetch, name="fetch")
]
