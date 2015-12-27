__author__ = 'chenbangjing'

"""hygiene URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
"""
from django.conf.urls import url
from index.views import index, register, do_register, login_page, do_login,logout

urlpatterns = [
    url(r'^$', index),
    url(r'^register/$', register),
    url(r'^do_register/$', do_register),
    url(r'^login/$', login_page),
    url(r'^do_login/$', do_login),
    url(r'^logout/', logout)
]