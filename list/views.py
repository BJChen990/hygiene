from django.http import HttpResponse, JsonResponse
from django.template import loader
from datetime import date as Date
from importing.models import Student, Class
from index.views import check_login
import json

# Create your views here.
@check_login
def list(request):
    t_header = loader.get_template('header.html')
    c_header = {'title': 'list'}

    if ('date' in request.GET.keys() and request.GET['date'] != ''):
        theDate = date_parser(request.GET['date'])
    else:
        theDate = Date.today().strftime('%Y-%m-%d')

    prequery = \
    """(SELECT the_class_id,name,date_schedule,student_id,id_in_class
        FROM `index_student`
        WHERE INSTR(`date_schedule`,'%s') )""" % theDate

    students = Class.objects.raw("""SELECT a.name as class_name, a.id, b.student_id, b.name, b.date_schedule, b.id_in_class
                                    FROM index_class  a, """+
                                    prequery + " b WHERE a.id = b.the_class_id;")

    class_container = {}
    for s in students:
        if s.class_name not in class_container.keys():
            class_container[s.class_name] = []
        s.today_status = json.JSONDecoder().decode(s.date_schedule)[theDate]
        class_container[s.class_name] += [s]

    t_content = loader.get_template('list.html')
    c_content = {'student_by_class':class_container, 'the_date':theDate}

    t_footer = loader.get_template('footer.html')
    c_footer = {}

    return HttpResponse(t_header.render(c_header) + t_content.render(c_content) + t_footer.render(c_footer) )

def date_parser(data_str):
    YY,MM,DD = data_str.split('-')
    int_year = int(YY)
    if int_year < 1911:
        YY = str(int_year+1911)
    return Date(int(YY),int(MM),int(DD)).strftime('%Y-%m-%d')

def complete(request):
    student_id = request.POST['student_id']
    the_date = date_parser(request.POST['date'])
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
    the_date = date_parser(request.POST['date'])

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
    the_date = date_parser(request.POST['date'])

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
