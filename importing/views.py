from django.shortcuts import render, redirect
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from importing.models import retreive_to_db

# Create your views here.
def import_page(request):
    return render(request,'import.html')

def upload(request):
    file = request.FILES['xls_file']
    path = default_storage.save('tmp.xls', ContentFile( file.read() ) )
    retreive_to_db(path)
    default_storage.delete(path)
    return redirect('/importing/')