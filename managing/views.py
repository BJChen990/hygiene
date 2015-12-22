from django.shortcuts import render
from django.http import JsonResponse
from django.core import serializers
from importing.models import Class

# Create your views here.
def index(request):
    return render(request, "index.html")

def request_classes(request, grade):
    classes = Class.objects.filter(grade=grade)
    data = serializers.serialize('json', classes)
    return JsonResponse(data,safe=False)

def byClass(request):
    print( request['POST'] )
    return