from django.http import HttpResponse, JsonResponse
from django.template import RequestContext, loader
from importing.models import Student
from json import JSONDecoder, JSONEncoder


# Create your views here.
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

