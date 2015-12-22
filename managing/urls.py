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
from managing.views import index, request_classes

urlpatterns = [
    url(r'^$', index, name='page'),
    url(r'^classes/(?P<grade>[1-3])/$', request_classes, name='classes')
]