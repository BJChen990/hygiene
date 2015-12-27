# -*- coding: utf-8 -*-

from django.http import HttpResponse, JsonResponse
from django.template import RequestContext, loader
from django.shortcuts import redirect
from importing.models import Student
from json import JSONDecoder, JSONEncoder
import math
from datetime import date as Date
from index.views import check_login


# Create your views here.
@check_login
def search_by_id(request,student_id):
    t_header = loader.get_template('header.html')
    c_header = RequestContext(request, {'title': 'list'})

    try:
        student = Student.objects.get(student_id = student_id)
        student.date_schedule = JSONDecoder().decode( student.date_schedule )
        finished_count = 0
        for key in student.date_schedule.keys():
            if student.date_schedule[key] == "Full":
                finished_count += 3
            elif student.date_schedule[key] == "OneThird":
                finished_count += 1

        student.day_last = student.should_come_count*3 - finished_count
        student.day_last = str(int(student.day_last / 3)) + "日" if student.day_last % 3 == 0 \
                    else str(math.floor(student.day_last/3))+"又"+ str(student.day_last % 3 )+"/3日"
        result = {'student' :  student }
    except:
        result = {'error': 'fail'}

    t_content = loader.get_template('search.html')
    c_content = RequestContext(request, result)

    t_footer = loader.get_template('footer.html')
    c_footer = RequestContext(request, {})

    return HttpResponse(t_header.render(c_header) + t_content.render(c_content) + t_footer.render(c_footer) )

def update(request):
    dates = JSONDecoder().decode( request.POST['theDates'] )
    student_id = request.POST['student-id']
    student = Student.objects.get(student_id=student_id)
    new_schedule = {}
    for date in dates.keys():
        new_schedule[date] = dates[date]
    student.date_schedule = JSONEncoder().encode(new_schedule)
    student.save()
    return JsonResponse({'success':'success'})

@check_login
def add(request):
    assigned_date = process_date(request.POST['date'])
    student_id = request.POST['student-id']
    type = request.POST['type']

    student = Student.objects.get(student_id = student_id)
    date_schedule = JSONDecoder().decode(student.date_schedule)

    finished_count = 0

    for key in date_schedule.keys():
        if date_schedule[key] == "Full":
            finished_count += 3
        elif date_schedule[key] == "OneThird":
            finished_count += 1

    day_last = student.should_come_count*3 - finished_count

    if assigned_date in date_schedule.keys():
        pass
    elif day_last <= 0:
        pass
    else:
        date_schedule[assigned_date] = type
        student.date_schedule = JSONEncoder().encode(date_schedule)
        student.save()
        return redirect('/search/id/'+str(student_id))


def process_date(date_str):
    YY,MM,DD = date_str.split('-')
    return Date(int(YY),int(MM),int(DD)).strftime('%Y-%m-%d')
