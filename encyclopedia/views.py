from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.http import HttpResponse
from . import util
import markdown2
from django.urls import reverse
import operator
from random import randrange


class SearchForm(forms.Form):
    pageTitle = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Search Encyclopedia', 'list': 'wiki', 'class': 'search'}), label='')


def index(request):
    return render(request, "encyclopedia/index.html", {
        "input": SearchForm(),
        "entries": util.list_entries()
    })


def handleForm(request):
    if request.method == 'GET':
        form = SearchForm(request.GET)
        if form.is_valid():
            pageTitle = form.cleaned_data['pageTitle']
            exists = util.get_entry(pageTitle)
            if exists:
                return HttpResponseRedirect(reverse('page', args=(pageTitle,)))
            suggestions = list(
                filter(lambda entry: pageTitle.lower() in entry.lower(), util.list_entries()))
            return render(request, 'encyclopedia/suggestions.html', {
                "input": SearchForm(),
                "entries": suggestions,
                "title": "Suggestions",
                "content": "<h1>Suggestions</h1>"
            })


def page(request, title):
    capTitle = title.capitalize()
    content = util.get_entry(capTitle)
    if content is not None:
        return render(request, 'encyclopedia/page.html', {
            "input": SearchForm(),
            "entries": util.list_entries(),
            "title": title.capitalize(),
            "content": markdown2.markdown(content)
        })
    return render(request, 'encyclopedia/page.html', {
        "input": SearchForm(),
        "entries": util.list_entries(),
        "title": "Not found",
        "content": "<h1>Requested page was not found</h1>"
    })


def newPage(request):
    if request.method == 'GET':
        return render(request, 'encyclopedia/newPage.html')
    elif request.method == 'POST':
        form = request.POST
        title = form['title']
        body = form['content']
        if not util.get_entry(title):
            util.save_entry(title, body)
            return HttpResponseRedirect(reverse('page', args=(title,)))
        return render(request, 'encyclopedia/page.html', {
            "input": SearchForm(),
            "entries": util.list_entries(),
            "title": 'Page already exist',
            "content": f'<h2>A page with title "{title}" already exists</h2>'
        })


def editPage(request):
    if request.method == 'GET':
        title = request.GET['title']
        return render(request, 'encyclopedia/EditPage.html', {
            "input": SearchForm(),
            "entries": util.list_entries(),
            "title": title,
            "content": util.get_entry(title)
        })
    elif request.method == 'POST':
        title = request.POST['title']
        body = request.POST['newBody']
        util.save_entry(title, body)
        return HttpResponseRedirect(reverse('page', args=(title,)))


def randomPage(request):
    titles = util.list_entries()
    randomTitle = titles[randrange(len(titles))]
    return HttpResponseRedirect(reverse('page', args=(randomTitle,)))
