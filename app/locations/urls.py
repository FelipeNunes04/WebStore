#coding: utf-8
from django.conf.urls.defaults import *
import views


urlpatterns = patterns('',
    url((r'^refresh-city/$'), views.refresh_city,
        name='refresh-city', ),
    url((r'^refresh-address/$'), views.refresh_address,
        name='refresh-address'),
)
