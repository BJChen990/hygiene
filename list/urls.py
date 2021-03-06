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
from list.views import list,complete, cancel, fail_the_rest

urlpatterns = [
    url(r'^$', list, name='page'),
    url(r'^date/$', list),
    url(r'complete/$', complete),
    url(r'cancel/$', cancel),
    url(r'fail_the_rest/$', fail_the_rest),

]