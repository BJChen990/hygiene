from django.shortcuts import render
from datetime import date as Date
from importing.models import Student

# Create your views here.
def list(request, date = "" ):
    YY,MM,DD = date.split("-") if date else ["","",""]
    theDate = YY+'-'+MM+'-'+DD if YY else Date.today().strftime('%Y-%m-%d')
    students = Student.objects.filter(date_to_come__contains=theDate)
    return render(request,'list.html',{'stu_list':students})
