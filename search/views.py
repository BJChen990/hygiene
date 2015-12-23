from django.shortcuts import render
from importing.models import Student
from django.http import JsonResponse
from django.core import serializers


# Create your views here.
def index(request):
    return render(request,'search.html')

def search_by_id(request,student_id):
    stu_id = student_id
    try:
        result = [Student.objects.get(student_id = stu_id)]
        data = serializers.serialize('json', result)
        return JsonResponse(data,safe=False)
    except:
        return JsonResponse({"error":"failed"})

