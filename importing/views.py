from django.shortcuts import render

# Create your views here.
def import_page(request):
    return render(request,'import.html')