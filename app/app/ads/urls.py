# coding: utf-8
from django.conf.urls.defaults import *
import views

urlpatterns = patterns('',

    url(r'^alterar-logo/(?P<slug>[-\w]+)/$',
        views.EditImageUpdateView.as_view(),
        name='edit_image', ),
    url(r'^alterar-fotos/(?P<slug>[-\w]+)/$', views.edit_photo_view,
        name='edit_photos', ),
    url(r'^alterar-video/(?P<slug>[-\w]+)/$',
        views.EditVideoUpdateView.as_view(),
        name='edit_video', ),
    url(r'^refresh-city/$', views.get_city,
        name='refresh_city'),
    url(r'^refresh-area/$', views.get_area,
        name='refresh_area'),
    url(r'^nova-assinatura/$', views.NewSignatureFormView.as_view(),
        name="new_signature"),
    url(r'^novo-anuncio/(?P<signature_id>\d+)$', views.NewAdFormView.as_view(),
        name='new_ad'),

    url(r'^filtrar-atividades-novo-anuncio/(?P<category_id>\d+)/(?P<ad_id>\d+)/$',
        views.activities_filter, name="activities_filter"),

    url(r'^filtrar-atividades/(?P<category_id>\d+)/(?P<ad_id>\d+)/$',
        views.activities_filter, name="activities_filter"),

    url(r'^filtrar-caracteristicas/(?P<ad_id>\d+)/$', views.values_filter,
        name="values_filter"),
    url(r'^carregar-imagem/$', views.image_upload, name="ad_image_upload"),
    url(r'^carregar-fotos/$', views.photos_upload, name="ad_photos_upload"),
    url(r'^excluir-imagems/$', views.images_delete, name="ad_image_delete"),
    url(r'^autorizar-comentario/(?P<pk>\d+)/$', views.authorize_comment,
        name='authorize_comment',),
    url(r'^bloquear-comentario/(?P<pk>\d+)/$', views.block_comment,
        name='block_comment', ),
    url(r'^desativar-anuncio/(?P<slug>[-\w]+)/$', views.disable_ad,
        name='disable_ad', ),
    url((r'^(?P<slug>[-\w]+)/$'), views.view_ad,
        name='ads_detail_view', ),
    url((r'^(?P<slug>[-\w]+)/editar/$'), views.EditAdUpdateView.as_view(),
        name='edit_ad', ),
)
