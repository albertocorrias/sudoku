from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from django.template import loader


def index(request):
    template = loader.get_template('sudoku_app/index.html')
    context = {
        'starting': 1
    }
    return HttpResponse(template.render(context, request))
