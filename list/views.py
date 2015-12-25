from django.http import HttpResponse
from django.template import RequestContext, loader

from datetime import date as Date
from importing.models import Student

# Create your views here.
def list(request, date = "" ):
    t_header = loader.get_template('header.html')
    c_header = RequestContext(request, {'title': 'list'})

    YY,MM,DD = date.split("-") if date else ["","",""]
    theDate = YY+'-'+MM+'-'+DD if YY else Date.today().strftime('%Y-%m-%d')
    students = Student.objects.filter(date_to_come__contains=theDate)

    t_content = loader.get_template('list.html')
    c_content = RequestContext(request, {'stu_list':students, 'today':theDate})

    t_footer = loader.get_template('footer.html')
    c_footer = RequestContext(request, {})

    return HttpResponse(t_header.render(c_header) + t_content.render(c_content) + t_footer.render(c_footer) )