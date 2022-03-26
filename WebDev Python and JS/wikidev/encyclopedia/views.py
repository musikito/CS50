import random
from turtle import title
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from markdown2 import Markdown
from django import forms


from . import util, forms
import encyclopedia

# Global var to be accessed by all funtions.
searchForm = forms.SearchForm()


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "search_form": searchForm
    })


def entry(request, title):

    md = util.get_entry(title)

    if md != None:

        entry_HTML = Markdown().convert(md)
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "entry": entry_HTML,
            "search_form": searchForm,
        })
    else:
        return render(request, "encyclopedia/404.html", {
            "title": title,
            "content": md,
            "search_form": searchForm
        })


def search(request):

    if request.method == "POST":
        form = forms.SearchForm(request.POST)

        # If form is valid try to search for title:
        if form.is_valid():
            title = form.cleaned_data["title"]
            md = util.get_entry(title)

            if md:
                # If entry exists, redirect to entry view
                return redirect(reverse('entry', args=[title]))
            else:
                # Otherwise display relevant search results
                related_titles = util.search_results(title)

                return render(request, "encyclopedia/result.html", {
                    "title": title,
                    "related_titles": related_titles,
                    "search_form": searchForm
                })

    # Otherwise form not posted or form not valid, return to index page:
    return redirect(reverse('index'))


def create_entry(request):
    """ Create a new page/entry """
    # We reached this part via a link, maybe from search? """
    if request.method == "GET":
        create_form = forms.CreateForm()
        return render(request, "encyclopedia/create_entry.html", {
            "form": searchForm,
            "create_form": create_form
        })
        # Else we submit a form via POST
    elif request.method == "POST":
        create_form = forms.CreateForm(request.POST)
        if create_form.is_valid():
            title = create_form.cleaned_data["title"]
            body = create_form.cleaned_data["body"]
        else:
            error_message = "No a valid entry, please try again"
            return render(request, "encyclopedia/create_entry.html", {
                "form": searchForm,
                "create_form": create_form,
                "error": error_message
            })
        # Check if entry already exist
        if util.get_entry(title):
            error_message = "Entry already exist, please edit it instead"
            return render(request, "encyclopedia/create_entry.html", {
                "form": searchForm,
                "create_form": create_form,
                "error": error_message
            })
        # save entry/file to disk
        else:
            util.save_entry(title, body)
            return redirect(reverse('entry', args=[title]))


def edit_entry(request, title):
    """Edit an existing entry"""
    # If reached via editing link, return form with post to edit:
    if request.method == "GET":
        text = util.get_entry(title)

        # Otherwise return pre-populated form:
        return render(request, "encyclopedia/edit_entry.html", {
            "title": title,
            "edit_form": forms.EditForm(initial={'text': text}),
            "search_form": searchForm
        })

    # If reached via posting form, updated page and redirect to page:
    elif request.method == "POST":
        form = forms.EditForm(request.POST)

        if form.is_valid():
            text = form.cleaned_data['text']
            util.save_entry(title, text)
            return redirect(reverse('entry', args=[title]))

        else:
            return render(request, "encyclopedia/edit.html", {
                "title": title,
                "edit_form": form,
                "search_form": searchForm
            })


def random_entry(request):
    """ Generates a new random page from entires"""
    # Make a list of entries and randonmize it
    titles = util.list_entries()
    title = random.choice(titles)

    return redirect(reverse('entry', args=[title]))
