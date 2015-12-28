# -*- coding: utf-8 -*-


from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.core import serializers
from importing.models import Class, Student
import json
from datetime import  date as Date
from index.views import check_login

# Create your views here.
@check_login
def index(request):
    t_header = loader.get_template('header.html')
    c_header = RequestContext(request, {'title': 'list'})

    grades = []
    grades += [Class.objects.filter(grade=1)]
    grades += [Class.objects.filter(grade=2)]
    grades += [Class.objects.filter(grade=3)]


    t_content = loader.get_template('managing.html')
    c_content = RequestContext(request, {'error':[],'grades':grades})

    t_footer = loader.get_template('footer.html')
    c_footer = RequestContext(request, {})

    return HttpResponse(t_header.render(c_header) + t_content.render(c_content) + t_footer.render(c_footer) )

def request_classes(request, grade):
    classes = Class.objects.filter(grade=grade)
    data = serializers.serialize('json', classes)
    return JsonResponse(data,safe=False)

def request_students(request, grade, number):
    the_class = Class.objects.get(grade=grade, number=number)
    students = the_class.student_set.all()
    data =serializers.serialize('json', students)
    return JsonResponse(data,safe=False)


@check_login
def schedule_date(request):
    decoder = json.JSONDecoder()

    err = []
    student_ids = decoder.decode( request.POST['students-id'] )
    assigned_date = process_date(request.POST['date'])

    students = Student.objects.filter(student_id__in=student_ids)
    for stu in students:
        date_schedule = decoder.decode(stu.date_schedule)

        finished_count = 0

        for key in date_schedule.keys():
            if date_schedule[key] == "Full":
                finished_count += 3
            elif date_schedule[key] == "OneThird":
                finished_count += 1

        day_last = stu.should_come_count*3 - finished_count

        if assigned_date in date_schedule.keys():
            err += [stu.name+u"在當天已經有排定掃地了"]
        elif day_last <= 0:
            err += [stu.name+u"已經掃滿了"]
        else:
            date_schedule[assigned_date] = "Pending"
            stu.date_schedule = json.JSONEncoder().encode(date_schedule)
            stu.save()


    t_header = loader.get_template('header.html')
    c_header = RequestContext(request, {'title': 'list'})

    t_content = loader.get_template('managing.html')
    c_content = RequestContext(request, {'error':err})

    t_footer = loader.get_template('footer.html')
    c_footer = RequestContext(request, {})

    return HttpResponse(t_header.render(c_header) + t_content.render(c_content) + t_footer.render(c_footer) )

@check_login
def read_only(request):
    t_header = loader.get_template('header.html')
    c_header = RequestContext(request, {'title': 'list'})

    t_content = loader.get_template('read_only.html')
    c_content = RequestContext(request, {})

    t_footer = loader.get_template('footer.html')
    c_footer = RequestContext(request, {})

    return HttpResponse(t_header.render(c_header) + t_content.render(c_content) + t_footer.render(c_footer) )

def process_date(date_str):
    YY,MM,DD = date_str.split('-')
    return Date(int(YY),int(MM),int(DD)).strftime('%Y-%m-%d')

def clear_all(request):
    Class.objects.all().delete()
    Student.objects.all().delete()
    return redirect('/list/')
