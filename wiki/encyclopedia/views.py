from django.http.response import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django import forms
from . import util
from markdown2 import Markdown

class allforms(forms.Form):
    
    title = forms.CharField(label="title", widget=forms.Textarea(attrs={'class': 'form-control col-md-8 col-lg-8', 'row': '3'}))
    content = forms.CharField(label="content", widget=forms.Textarea(attrs={'class': 'form-control col-md-8 col-lg-8', 'row':'10'}))
    edit = forms.BooleanField(initial=False, widget=forms.HiddenInput(), required=False)


def index(request):
    enteris = util.list_entries()
    return render(request, "encyclopedia/index.html", {
        "entries": enteris
    })

def entry(request, entry):
    entryPage= util.get_entry(entry)
    markdowner = Markdown()
    if entryPage is None:
        return render(request, "encyclopedia/nonexistanceEntry.html",{
            "entrytitle": entry
        })
    else:
        return render(request, "encyclopedia/entry.html", {
        "entry": markdowner.convert(entryPage),
        "entrytitle": entry
        # "entry": entryPage

    })
def addpage(request):
    if request.method == "POST":
        form = allforms(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            if (util.get_entry(title) is None or form.cleaned_data["edit"] is True):
                util.save_entry(title, content)
                return HttpResponseRedirect(reverse("entry", kwargs={'entry': title}))
            else:
                return render(request, "encyclopedia/addpage.html",{
                    "form": form,
                    "existing": True,
                    "entry": title
                })
        else:
            return render(request, "encyclopedia/addpage.html", {
                "form": form,
                "existing": False
            })
    else:
        return render(request, "encyclopedia/addpage.html", {
            "form": allforms(),
            "existing": False
           
        })
def edit(request, entry):
    entrypage = util.get_entry(entry)
    if entrypage is None:
        return render(request, "encyclopedia/nonexistanceEntry.html",{
            "entrytitle": entry
        })
    else:
        form = allforms()
        form.fields["title"].intial = entry
        form.fields["title"].widget = forms.HiddenInput()
        form.fields["content"].intial = entrypage
        form.fields["edit"].intial = True
        return render(request, "encyclopedia/addpage.html", {
            "form": form,
            "edit": form.fields["edit"].intial,
            "entrytitle": form.fields["title"].intial
        })

def searchentry(request):
    value = request.GET.get('q', '')
    if (util.get_entry(value) is not None):
        return HttpResponseRedirect(reverse("entry", kwargs={'entry': value}))

    else:
        entrysubstring = []
        for entry in util.list_entries():
            if value.upper() in entry.upper():
                entrysubstring.append(entry)

        return render(request, "encyclopedia/index.html",{
            "entries": entrysubstring,
            "search": True,
            "value": value
        })

