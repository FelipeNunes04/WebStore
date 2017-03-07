#coding: utf-8
from django.conf.urls.defaults import *
import views


urlpatterns = patterns('',
    url(r'^(?P<slug>[-\w]+)/nova-promocao/$',
        views.PromotionFormView.as_view(), name='new_promotion', ),
    url(r'^meus-cupons/$', views.MyPromotionListView.as_view(),
        name='my_promotions', ),
    url(r'^detalhe/(?P<pk>\d+)/$', views.PromotionDetailView.as_view(),
        name='my_promotion_detail', ),
    url(r'^desativar-cupom/(?P<pk>\d+)/$', views.disable_promotion,
        name='disable_promotion', ),
    url(r'^gerar-cupom/(?P<pk>\d+)/$', views.VoucherCreateView.as_view(),
        name='create_code', ),
    url(r'gerar-voucher-pdf/(?P<pk>\d+)/$', views.voucher_pdf,
        name='create_voucher_pdf', ),
    url(r'todas-promocoes/$', views.AllPromotionListView.as_view(),
        name='all_promotions', ),

    url(r'^teste/(?P<pk>\d+)/$', views.TesteDetailView.as_view(),
        name='teste', ),
)
