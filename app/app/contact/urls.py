# coding: utf-8
from django.conf.urls.defaults import *
from django.views.generic import TemplateView
import views

urlpatterns = patterns('',
    url(r'^$', views.ContactFormView.as_view(), name='contact_form'),
)
