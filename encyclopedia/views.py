from django.shortcuts import render
import markdown2

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