from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
import markdown2
from django.urls import reverse

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    md_file = util.get_entry(title)
    if bool(md_file):
        html_file = markdown2.markdown(md_file)
        return render(request, "encyclopedia/entry.html", {
            "body": html_file,
            "entry": title
    })
    return render(request, "encyclopedia/entry_error.html")

def search(request):
    #Getting query from Post methond in the form
    query = request.POST["q"]   

    #If the query matches an entry, then display the entry
    if query in util.list_entries():
        return entry(request, query)

    #If the query does not matches an entry, display list with similar entries
    similar_entries = [entry for entry in util.list_entries() if query in entry]
    return render(request, "encyclopedia/search.html", {
        "query": query,
        "similar_entries": similar_entries
    })

def newpage(request):
    return render(request, "encyclopedia/newpage.html")