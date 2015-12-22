from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.core import serializers
from importing.models import Class, Student
import json

# Create your views here.
def index(request):
    return render(request, "index.html", context={'error':[]})

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
    decoder = json.JSONDecoder()
    err = []
    ids = decoder.decode( request.POST['students-id'] )
    date = request.POST['date']
    students = Student.objects.filter(student_id__in=ids)
    for stu in students:
        dates = decoder.decode(stu.date_to_come)
        if len(dates) >= 3:
            err += [stu.name+"已經掃滿了"]
        elif date in dates:
            err += [stu.name+"在當天已經有排定掃地了"]
        else:
            dates += [date]
            stu.date_to_come = json.JSONEncoder().encode(dates)
            stu.times_remain_to_clean -= 1
            stu.save()

    return render(request, "index.html", context={'error':err} )
