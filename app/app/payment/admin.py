# coding: utf-8
from django.contrib import admin
from models import Payment


class PaymentAdmin(admin.ModelAdmin):
    list_display = ('name', )
    prepopulated_fields = {
        'slug': ('name', ) 
    }
    search_fields = ('name', )

admin.site.register(Payment, PaymentAdmin)
