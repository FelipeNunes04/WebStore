# coding: utf-8
from django.contrib import admin
from models import City, Area, ZipCode, State


class AreaAdmin(admin.ModelAdmin):
    list_display = ('area', 'city', )
    search_fields = ('area', 'id', )
    raw_id_fields = ('city', )


class CityAdmin(admin.ModelAdmin):
    list_display = ('city', 'state', )
    list_filter = ('state', )
    search_fields = ('city',)


class ZipCodeAdmin(admin.ModelAdmin):
    list_display = ('zip_code', 'city', )
    search_fields = ('zip_code', )


class StateAdmin(admin.ModelAdmin):
    list_display = ('id', 'state', )
    list_display_links = ('id', 'state',)

admin.site.register(ZipCode, ZipCodeAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(Area, AreaAdmin)
admin.site.register(State, StateAdmin)
