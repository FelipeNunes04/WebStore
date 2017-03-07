# coding: utf-8
from django.conf.urls.defaults import *

import views

urlpatterns = patterns('',
    url((r'^filtro/$'), views.result_filter, name='result_filter', ),
    url((r'^(?P<slug>[-\w]+)/$'), views.CategoryDetailView.as_view(),
        name='category_detail_view', ),
)
