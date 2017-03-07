# coding: utf-8
from django.contrib import admin
from datetime import datetime
from models import Plan, Ad, Photo, Signature
from forms import AdminEditAdForm


class PlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'days', 'value_ad', )
    list_filter = ('days',)
    search_fields = ('name', )


class SignatureAdmin(admin.ModelAdmin):
    list_display = ('plan', 'customer', 'number_ads', 'value_signature',
                    'start_date', 'end_date', 'is_active', )
    readonly_fields = ('end_date', 'number_ads_available', )
    list_filter = ('plan', )
    date_hierarchy = 'start_date'
    list_filter = ('is_active',)


class PhotoInline(admin.TabularInline):
    model = Photo
    extra = 0
    max_num = 6


class AdAdmin(admin.ModelAdmin):
    form = AdminEditAdForm
    list_display = ('fancy_name', 'is_active', 'signature',
                    'signature_is_active', 'city', 'area', 'is_national',
                    'category', )
    inlines = [PhotoInline]
    list_filter = ('category', 'is_active', )
    prepopulated_fields = {
        'slug': ('fancy_name', ),
        }
    raw_id_fields = ('city', 'state', 'activities', 'option_values',
        'payment', )
    # readonly_fields = ('views', 'category', 'activities', 'option_values',
    #                     'signature', 'user', )
    search_fields = ('fancy_name',)
    # list_editable = ('is_active', )

    def signature_is_active(self, obj):
        now = datetime.now()
        signature = obj.signature
        return (signature.is_active == True) and\
                (signature.end_date >= now)and\
                (signature.start_date <= now)
    signature_is_active.short_description = u'Assinatura ativa'
    signature_is_active.boolean = True

    class Media:
        js = [
                'admin/js/base.js',
                'js/lib/jquery.masked.js'
            ]

admin.site.register(Plan, PlanAdmin)
admin.site.register(Ad, AdAdmin)
admin.site.register(Signature, SignatureAdmin)
