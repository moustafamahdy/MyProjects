from unicodedata import name
from django.urls import path

from . import views
# app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("add", views.addpage, name="addpage"),
    path("wiki/<str:entry>", views.entry, name="entry"),
    path("wiki/<str:entry>/edit", views.edit, name="edit"),
    path("search", views.searchentry, name="search")
]
