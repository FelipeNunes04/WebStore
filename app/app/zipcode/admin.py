# coding: utf-8
from django.contrib import admin
from models import ZipCode


class ZipCodeAdmin(admin.ModelAdmin):
    list_display = ('zip_code', 'city', 'state', )
    search_fields = ('city', 'address', 'neighborhood', )

admin.site.register(ZipCode, ZipCodeAdmin)
