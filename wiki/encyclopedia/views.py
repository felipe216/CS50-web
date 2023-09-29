from django.shortcuts import render, redirect
from markdown2 import Markdown
from django import forms
from django.contrib import messages
from django.urls import reverse
from random import choice


from . import util


class SearchForm(forms.Form):
    """ Form Class for Search Bar """
    title = forms.CharField(label='', widget=forms.TextInput(attrs={
      "class": "search",
      "placeholder": "Search Qwikipedia"}))



class EditForm(forms.Form):
    text = forms.CharField(label='', widget=forms.Textarea(attrs={
        "placeholder": "Enter Page Content using Markdown"
    }))



class CreateForm(forms.Form):
    title = forms.CharField(label='', widget=forms.TextInput(attrs={
      "class": "search",
      "placeholder": "Title"}))
    text = forms.CharField(label='', widget=forms.Textarea(attrs={
        "placeholder": "Enter Page Content using Markdown"
    }))

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def render_wiki(request, title):
    entry = util.get_entry(title)

    if entry != None:
        entry_html = Markdown().convert(entry)
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "entry": entry_html,
            "search_form": SearchForm(),
        })
    else:
        return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    }) 




def edit(request, title):
    if request.method == "GET":
        text = util.get_entry(title)

        if text == None:
            messages.error(request, f"{title} page does not exist can't be edited!")

        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "edit_form":
            EditForm(initial={'test': text}),
            "search_form": SearchForm()
        })
    
    elif request.method == "POST":
        form = EditForm(request.POST)

        if form.is_valid():
            text = form.cleaned_data['text']
            util.save_entry(title, text)
            messages.success(request, f"Entry {title} updated!")
            return redirect(reverse('render_wiki', args=[title]))
        else:
            messages.error(request, f'Editing form not valid, please try again!')
            return render(request, "encyclopedia/edit.html", {
            "title": title,
            "edit_form": form,
            "search_form": SearchForm()
          })




def search(request):
    if request.method == "GET":
        return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

    elif request.method == "POST":
        title = request.POST['title']
        return redirect(reverse('render_wiki', args=[title]))
    

def create(request):
    if request.method == "GET":
        return render(request, "encyclopedia/create.html", {
            "create_form": CreateForm(),
            "search_form": SearchForm()
        })
    
    elif request.method == "POST":
        title = request.POST['title']
        content = request.POST['text']

        if util.get_entry(title) == None:
            util.save_entry(title, content)
            return redirect(reverse('render_wiki', args=[title]))
        else:
            messages.add_message(request, messages.ERROR, f"{title} already exist!")
            return redirect(reverse('create'))



def random(request):
    entries = util.list_entries()
    title = choice(entries)

    return redirect(reverse('render_wiki', args=[title]))