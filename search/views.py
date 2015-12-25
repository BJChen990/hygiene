from django.http import HttpResponse
from django.template import RequestContext, loader
from importing.models import Student
from json import JSONDecoder


# Create your views here.
def search_by_id(request,student_id):
    t_header = loader.get_template('header.html')
    c_header = RequestContext(request, {'title': 'list'})

    try:
        student = Student.objects.get(student_id = student_id)
        student.date_to_come = JSONDecoder().decode( student.date_to_come )
        result = {'student' :  student }
    except:
        result = {'error': 'fail'}

    t_content = loader.get_template('search.html')
    c_content = RequestContext(request, result)

    t_footer = loader.get_template('footer.html')
    c_footer = RequestContext(request, {})

    return HttpResponse(t_header.render(c_header) + t_content.render(c_content) + t_footer.render(c_footer) )

