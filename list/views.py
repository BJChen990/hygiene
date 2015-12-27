from django.http import HttpResponse, JsonResponse
from django.template import RequestContext, loader

from datetime import date as Date
from importing.models import Student
import json


# Create your views here.
def list(request):

    t_header = loader.get_template('header.html')
    c_header = RequestContext(request, {'title': 'list'})

    theDate = request.GET['date'] if ('date' in request.GET.keys() and request.GET['date'] != '') \
                                  else Date.today().strftime('%Y-%m-%d')

    students = Student.objects.filter(date_schedule__contains=theDate)
    for stu in students:
        stu.today_status = json.JSONDecoder().decode(stu.date_schedule)[theDate]

    t_content = loader.get_template('list.html')
    c_content = RequestContext(request, {'stu_list':students, 'today':theDate})

    t_footer = loader.get_template('footer.html')
    c_footer = RequestContext(request, {})

    return HttpResponse(t_header.render({'title': 'list'}) + t_content.render({'stu_list':students, 'today':theDate}) + t_footer.render({}) )

def complete(request):
    student_id = request.POST['student_id']
    the_date = request.POST['date'] if ('date' in request.POST.keys() and request.POST['date'] != '') \
                                    else Date.today().strftime('%Y-%m-%d')
    print(the_date)
    try:
        student = Student.objects.get(student_id=student_id)
        new_schedule = json.JSONDecoder().decode(student.date_schedule)
        for date in new_schedule:
            if date == the_date and new_schedule[date] not in ('Full', 'OneThird'):
                new_schedule[date] = "Full"
                student.date_schedule = json.JSONEncoder().encode(new_schedule)
                student.save()
                return JsonResponse({'success':'success'})
        return JsonResponse({'error':'today not in schedule'})
    except:
        return JsonResponse({'error':'undefined error'})

def cancel(request):
    student_id = request.POST['student_id']
    the_date = request.POST['date'] if ('date' in request.POST.keys() and request.POST['date'] != '') \
                                    else Date.today().strftime('%Y-%m-%d')
    try:
        student = Student.objects.get(student_id=student_id)
        new_schedule = json.JSONDecoder().decode(student.date_schedule)
        for date in new_schedule:
            if date == the_date and new_schedule[date] in ('Full', 'OneThird'):
                new_schedule[date] = "Pending"
                student.date_schedule = json.JSONEncoder().encode(new_schedule)
                student.save()
                return JsonResponse({'success':'success'})
        return JsonResponse({'error':'today not in schedule'})
    except:
        return JsonResponse({'error':'undefined error'})

def fail_the_rest(request):
    student_ids = json.JSONDecoder().decode(request.POST['student_ids'])
    the_date = request.POST['date'] if ('date' in request.POST.keys() and request.POST['date'] != '') \
                                    else Date.today().strftime('%Y-%m-%d')

    decoder = json.JSONDecoder()
    encoder = json.JSONEncoder()
    try:
        students = Student.objects.filter(student_id__in=student_ids)
        for student in students:
            new_schedule = decoder.decode(student.date_schedule)
            for date in new_schedule:
                if date == the_date and new_schedule[date] == "Pending":
                    new_schedule[date] = "Fail"
                    student.date_schedule = encoder.encode(new_schedule)
                    student.save()
        return JsonResponse({'success':'success'})
    except:
        return JsonResponse({'error':'undefined error'})
