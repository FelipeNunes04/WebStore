# coding: utf-8
from django.contrib import admin
from datetime import datetime
from models import Banner, CarouselHome


class BannerAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'city', 'start_date', 'end_date',
                    'is_national', 'is_active', 'banner_is_active')
    list_filter = ('category', )
    raw_id_fields = ('city', )
    readonly_fields = ('date_added', )
    search_fields = ('name', )

    def banner_is_active(self, obj):
        now = datetime.now()
        return (obj.end_date >= now) and (obj.start_date <= now)
    banner_is_active.short_description = u'Exibido'
    banner_is_active.boolean = True


class CarouselHomeAdmin(admin.ModelAdmin):
    list_display = ('name', 'link', 'city', 'start_date', 'end_date',
                    'is_national', 'is_active', 'carousel_home_is_active')
    raw_id_fields = ('city', )
    readonly_fields = ('date_added', )
    search_fields = ('name', )

    def carousel_home_is_active(self, obj):
        now = datetime.now()
        return (obj.end_date >= now) and (obj.start_date <= now)
    carousel_home_is_active.short_description = u'Exibido'
    carousel_home_is_active.boolean = True


admin.site.register(Banner, BannerAdmin)
admin.site.register(CarouselHome, CarouselHomeAdmin)
