from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import render, redirect
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from importing.models import retreive_to_db

# Create your views here.
def import_page(request):
    t_header = loader.get_template('header.html')
    c_header = RequestContext(request, {'title': 'list'})

    t_content = loader.get_template('import.html')
    c_content = RequestContext(request, {})

    t_footer = loader.get_template('footer.html')
    c_footer = RequestContext(request, {})

    return HttpResponse(t_header.render(c_header) + t_content.render(c_content) + t_footer.render(c_footer) )


def upload(request):
    file = request.FILES['xls_file']
    path = default_storage.save('tmp.xls', ContentFile( file.read() ) )
    retreive_to_db(path)
    default_storage.delete(path)
    return redirect('/importing/')
