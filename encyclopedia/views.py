#from logging import _FormatStyle
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
import markdown2
from django.urls import reverse
from django import forms

from . import util

class NewPageForm(forms.Form):
    title = forms.CharField(label= "Tilte", widget=forms.TextInput(attrs={'placeholder': 'Title'}))
    content = forms.CharField(label= "Content", widget=forms.Textarea(attrs={'placeholder': 'Content'}))

class EditForm(forms.Form):
    content = forms.CharField(label= "", widget=forms.Textarea())


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
    #Booloean var to check whether we are adding a new entry
    new_entry = True

    if request.method == "POST":

        # Take in the data the user submitted and save it as form
        form = NewPageForm(request.POST)

        # Check if form data is valid (server-side)
        if form.is_valid(): 

            # Isolate the title and the content from the form                        
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            
            #Check wheter it is a new entry
            if title in util.list_entries():
                new_entry = False
            else:
                #Create a new file
                f = open(f"entries/{title}.md", 'x')
                f.write(content)
                f.close()

                #display new page
                return entry(request, title)
            

    return render(request, "encyclopedia/newpage.html", {
        "new_entry": new_entry,
        "form": NewPageForm()
    })


def editpage(request, title):

    if request.method == "GET":  
        #Getting the markdown text of the entry
        md_file = util.get_entry(title)

        #Creating textarea with this text
        form = EditForm(initial={'content': md_file})

        #rendering the view
        return render(request, "encyclopedia/editpage.html", {
            "entry": title,
            "text_box": form
        })

    else:
        # Take in the data the user submitted and save it as form
        new_form = EditForm(request.POST)
        
        # Check if form data is valid (server-side)
        if new_form.is_valid():

            # Isolate the title and the content from the form                        
            new_content = new_form.cleaned_data["content"]

            #Open the file an overwrite it
            f = open(f"entries/{title}.md", 'w')
            f.write(new_content)
            f.close()

            #display edited page
            return entry(request, title)


    