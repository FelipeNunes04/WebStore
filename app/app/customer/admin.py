# coding: utf-8
from django.contrib import admin
from models import Customer, Advertiser, UserProfile


class CustomerAdmin(admin.ModelAdmin):
    exclude = ('password',)
    list_display = ('name', 'email', 'area_phone', 'phone', 'city', 'state', )
    raw_id_fields = ('user', )
    search_fields = ('name', )
    list_filter = ('city', 'state', )


class AdvertiserAdmin(admin.ModelAdmin):
    exclude = ('password',)
    list_display = ('name', 'type_person', 'cpf_cnpj', 'email', 'responsible',
                            'area_phone', 'phone', 'city', 'state', )
    raw_id_fields = ('user', )
    search_fields = ('name', )
    list_filter = ('city', 'state', )


admin.site.register(Customer, CustomerAdmin)
admin.site.register(Advertiser, AdvertiserAdmin)
