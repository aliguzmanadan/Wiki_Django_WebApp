from django.urls import path
from . import views
import encyclopedia
import re

app_name = "encyclopedia"

urlpatterns = [
    path("", views.index, name="index"),
    path("search", views.search, name="search"),
    path("newpage", views.newpage, name="newpage"),
    path(r'^editpage/(?P<title>\w)', views.editpage, name="editpage"),
    path("randompage", views.randompage, name="randompage"),
    path("<str:title>", views.entry, name="entry")
]
