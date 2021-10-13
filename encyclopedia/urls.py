from django.urls import path

from . import views
import encyclopedia

app_name = "encyclopedia"

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:title>", views.entry, name="entry")
]
