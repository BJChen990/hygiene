from django.http import HttpResponse, JsonResponse
from django.template import loader
from datetime import date as Date
from importing.models import Student
from index.views import check_login
import json



# Create your views here.
@check_login
def list(request):
    t_header = loader.get_template('header.html')
    c_header = {'title': 'list'}

    theDate = process_date(request.GET['date']) if ('date' in request.GET.keys() and request.GET['date'] != '') \
                                  else Date.today().strftime('%Y-%m-%d')
    year,month,date = theDate.split('-')

    students = Student.objects.filter(date_schedule__contains=theDate)
    for stu in students:
        stu.today_status = json.JSONDecoder().decode(stu.date_schedule)[theDate]

    t_content = loader.get_template('list.html')
    c_content = {'stu_list':students, 'the_date':{'Y':year,'M':month,'D':date}}

    t_footer = loader.get_template('footer.html')
    c_footer = {}

    return HttpResponse(t_header.render(c_header) + t_content.render(c_content) + t_footer.render(c_footer) )


def process_date(date_str):
    YY,MM,DD = date_str.split('-')
    return Date(int(YY),int(MM),int(DD)).strftime('%Y-%m-%d')

def complete(request):
    student_id = request.POST['student_id']
    the_date = process_date(request.POST['date'])
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
    the_date = process_date(request.POST['date'])

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
    the_date = process_date(request.POST['date'])

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
