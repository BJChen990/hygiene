from django.shortcuts import render, redirect

# Create your views here.
def import_page(request):
    return render(request,'import.html')

def upload(request):
    print(request)
    return redirect('/')