# coding: utf-8
from django.conf.urls.defaults import *
from views import VideoDetailView
import views

urlpatterns = patterns('',
    url((r'^categoria/(?P<slug>[-\w]+)/$'), views.VideoRefreshTemplateView.as_view(),
        name='video_refresh_view', ),
    url((r'^(?P<slug>[-\w]+)/$'), views.VideoDetailView.as_view(),
        name='video_detail_view', ),
)
