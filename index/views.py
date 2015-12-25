from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from datetime import date as Date
from list.views import list

# Create your views here.
def index(request):
    return list(request)