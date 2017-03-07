# coding: utf-8
from django.conf.urls.defaults import *
from django.contrib.auth.views import login, logout
import views

urlpatterns = patterns('',
    url(r'^login/$', login, {
        'template_name': 'customer/login.html',
        }, name='customer_signin'),

    url(r'^logout/$', logout, {
        'template_name': 'appsite/home.html',
        'next_page': '/',
        }, name='customer_signout'),
    url(r'^cadastro/$', views.CustomerFormView.as_view(),
            name='customer_registration'),
    url(r'^cadastro-com-sucesso/$', views.SuccessRegistrationView.as_view(),
            name='success_registration'),
    url(r'^editar-cadastro/$', views.EditRegistrationView.as_view(),
            name='edit_registration'),
    url(
        r'^cadastro-editado-com-sucesso/$',
        views.SuccesEditRegistrationView.as_view(),
        name='succes_edit_registration'
        ),
    url(r'^meus-anuncios/$', views.MyAdsFormView.as_view(),
            name='my_ads'),
    url(r'^cadastro-anunciante/$', views.AdvertiserFormView.as_view(),
            name='contact_advertiser_form'),
    url(r'^esqueci-minha-senha/$', views.ForgotPasswordView.as_view(),
            name='forgot_password'),
)
