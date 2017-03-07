# coding: utf-8
from django.conf.urls.defaults import *
from django.views.generic import TemplateView, ListView

import views

urlpatterns = patterns('',
    url(r'^$', views.PollView.as_view(), name='polls_view'),
    url(r'^result/(?P<id>\d+)/(?P<created>\d+)/$', \
        views.PollResultView.as_view(),\
        name='polls_result_view', )
    )
