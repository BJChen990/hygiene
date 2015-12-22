from django.shortcuts import render
from django.http import JsonResponse
from django.core import serializers
from importing.models import Class, Student

# Create your views here.
def index(request):
    return render(request, "index.html")

def request_classes(request, grade):
    classes = Class.objects.filter(grade=grade)
    data = serializers.serialize('json', classes)
    return JsonResponse(data,safe=False)

def request_students(request, grade, number):
    the_class = Class.objects.get(grade=grade, number=number)
    students = the_class.student_set.all()
    data =serializers.serialize('json', students)
    return JsonResponse(data,safe=False)

def schedule_date(request):
    
    return JsonResponse({'1':1})
