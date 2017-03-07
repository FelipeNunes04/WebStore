from os import path as os_path
from django.conf import settings
from django.conf.urls.defaults import *
from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from django.views.generic.simple import direct_to_template

import haystack


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^anuncio/', include('ads.urls')),
    url(r'^search/', include('haystack.urls')),
    url(r'^tv/', include('channel.urls')),
    url(r'^categoria/', include('category.urls')),
    url(r'^cliente/', include('customer.urls')),
    url(r'^comentarios/', include('django.contrib.comments.urls')),
    url(r'^contato/', include('contact.urls')),
    url(r'^dicas/', include('news.urls')),
    url(r'^enquete/', include('polls.urls')),
    url(r'^locations/', include('locations.urls')),
    url(r'^promocao/', include('voucher.urls')),
    url(r'^zipcode/', include('zipcode.urls')),
    (r'^retornacep.json', 'wqti_util.cep.retorna_cep', {'SSL': True}),



    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('appsite.urls')),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(.*)$', 'django.views.static.serve', {
            'document_root': os_path.join(settings.PROJECT_PATH, 'media'),
        }),
    )
