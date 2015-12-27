# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import RequestContext, loader

from index.models import User
import bcrypt


def check_login(func):
    def check_session(*args,**kwargs):
        request = args[0]
        return func(*args,**kwargs) if ('user' in request.session.keys() ) else redirect('/login/')
    return check_session

# Create your views here.
def index(request):
    return redirect('/list/')

def register(request):
    try:
        user = User.objects.get(type="root")
        has_root = True
    except:
        has_root = False

    if has_root:
        if 'type' not in request.session.keys() or request.session['type'] != 'root':
            return redirect('/')
        c_content = {'shouldHaveRoot': True}
    else:
        c_content = {'shouldHaveRoot': False}

    print(c_content)
    t_header = loader.get_template('header.html')
    c_header = {'title': '註冊'}

    t_content = loader.get_template('register.html')

    t_footer = loader.get_template('footer.html')
    c_footer = {}

    return HttpResponse(t_header.render(c_header) + t_content.render(c_content,request) + t_footer.render(c_footer) )

def do_register(request):
    if request.POST['pwd'] and request.POST['student-id']:
        student_id = request.POST['student-id']
        pwd = bcrypt.hashpw( request.POST['pwd'].encode('utf-8') , bcrypt.gensalt() )
        if request.POST['type'] == 'root':
            try:
                user = User.objects.get(type='root')
                return redirect('/register/')
            except:
                user = User(user_id=student_id,password = pwd, type=request.POST['type'])
                user.save()
                return redirect('/login/')
        else:
            user = User(user_id=student_id,password = pwd, type=request.POST['type'])
            user.save()
            return redirect('/login/')
    else:
        return redirect('/register/')

def login_page(request):
    t_header = loader.get_template('header.html')
    c_header = {'title': '登入'}

    t_content = loader.get_template('login.html')
    c_content = {}

    t_footer = loader.get_template('footer.html')
    c_footer = {}

    return HttpResponse(t_header.render(c_header) + t_content.render(c_content,request) + t_footer.render(c_footer) )

def do_login(request):
    if request.POST['pwd'] and request.POST['student-id']:
        student_id = request.POST['student-id']
        user = User.objects.get(user_id=student_id)
        if bcrypt.hashpw( request.POST['pwd'].encode('utf-8'), user.password.encode('utf-8') ):
            request.session.set_expiry(3600)
            request.session['user'] = student_id
            request.session['type'] = user.type
            return redirect('/')
    else:
        return redirect('/login/')

def logout(request):
    request.session.flush()
    return redirect('/login/')

