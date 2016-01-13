# -*- coding: utf-8 -*-


from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.core import serializers
from django.db import connection
from importing.models import Class, Student
import json

from datetime import  date as Date
from index.views import check_login

# Create your views here.
decoder = json.JSONDecoder()



def left_days(student):
    try:
        date_schedule = decoder.decode(student['date_schedule'])
    except:
        date_schedule = decoder.decode(student.date_schedule)

    finished_count = 0
    for key in date_schedule.keys():
        if date_schedule[key] == "Full":
            finished_count += 3
        elif date_schedule[key] == "OneThird":
            finished_count += 1
    try:
        return student['should_come_count']*3 - finished_count
    except:
        return student.should_come_count*3 - finished_count


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

    cursor = connection.cursor()
    cursor.execute('''SELECT * FROM `index_class` WHERE grade = %s;'''% grade )
    classes = dictfetchall(cursor)
    data = json.JSONEncoder().encode(classes)
    return JsonResponse(data,safe=False)

def request_students(request, grade, number):
    cursor = connection.cursor()
    cursor.execute('''SELECT a.*, b.name as class_name
                      FROM
                        (SELECT * FROM `index_class` WHERE grade = %s AND number = %s) b,
                        `index_student` a
                      WHERE a.the_class_id = b.id''' % (grade,number) )
    students = dictfetchall(cursor)
    data = json.JSONEncoder().encode(students)
    return JsonResponse(data,safe=False)

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def request_uncomming_students(request, grade):

    cursor = connection.cursor()

    prequery = \
    """(SELECT the_class_id,name,date_schedule,student_id,id_in_class, should_come_count
        FROM `index_student`
        WHERE INSTR(`date_schedule`,'Fail') )"""

    cursor.execute("""SELECT a.name as class_name, a.id, b.student_id, b.should_come_count, b.name, b.date_schedule, b.id_in_class
                                    FROM `index_class` a, """+
                                    prequery + " b WHERE a.id = b.the_class_id AND a.grade = %s ORDER BY class_name;" % grade)

    students = dictfetchall(cursor)
    students = [ student for student in students if left_days(student) > 0 ]
    data = json.JSONEncoder().encode(students)
    return JsonResponse(data,safe=False)

@check_login
def schedule_date(request):

    err = []
    student_ids = decoder.decode( request.POST['students-id'] )
    assigned_date = process_date(request.POST['date'])

    students = Student.objects.filter(student_id__in=student_ids)
    for stu in students:
        date_schedule = decoder.decode(stu.date_schedule)

        day_last = left_days(stu)

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

@check_login
def clear_schedule(request):
    Student.objects.all().update(date_schedule='{}')
    return redirect('/')

@check_login
def clear_all(request):
    Class.objects.all().delete()
    Student.objects.all().delete()
    return redirect('/list/')
