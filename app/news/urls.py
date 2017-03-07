# coding: utf-8
from django.conf.urls.defaults import *
from views import EntryDetailView
import views

urlpatterns = patterns('',
    url(r'^(?P<slug>[-\w]+)/$', views.EntryDetailView.as_view(), 
                                                        name='entry_detail'),
)
