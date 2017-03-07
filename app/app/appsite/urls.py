#coding: utf-8
from django.conf.urls.defaults import *
import views


urlpatterns = patterns('',
    (r'^admin/image_upload/upload/$', 'appsite.admin.image_upload'),
    url(r'^institucional/$', views.CorporateTemplateView.as_view(),
                    name='appsite_corporate', ),
    url(r'^politica-de-privacidade/$', views.PrivacyTemplateView.as_view(),
                    name='appsite_privacy', ),
    url(r'^termos-de-uso/$', views.TermsOfUseTemplateView.as_view(),
                    name='appsite_terms_of_use', ),
    url(r'^admin/image_upload/$', views.image_upload,
                    name='image_upload', ),
    url(r'^resultado-busca/$', views.result_search,
                    name='result_search', ),
    # url(r'^resultado-filtro/$', views.result_filter_category,
    #                 name='result_filter_category', ),
    url(r'^sugestao/$', views.suggestion,
                    name='suggestion', ),
    url(r'^$', views.HomeTemplateView.as_view(),
                    name='appsite_home', ),
    url(r'^denuncia-sucesso/$', views.ReportSuccessTemplateView.as_view(),
                    name='report_success_view', ),
    url(r'^denuncie/(?P<comment_pk>\d+)/$', views.ReportFormView.as_view(),
                    name='report_view', ),
)
