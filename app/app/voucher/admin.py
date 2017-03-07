#coding: utf-8
from django.contrib import admin
from django.utils.datetime_safe import datetime
from models import Promotion


class PromotionAdmin(admin.ModelAdmin):
    list_display = ('title','id', 'ad', 'end_date', 'active_date', 'limit_vouchers',
                    'coupons', 'is_active', )
    list_filter = ('is_active', )
    readonly_fields = ('ad', 'title', 'description',
                        'discount', 'price', 'discouted_price',
                        'coupons', 'limit_vouchers', 'rules', 'is_active')
    search_fields = ('title', 'description', )
    list_editable = ('is_active', )

    def active_date(self, obj):
        if obj.end_date and obj.start_date:
            return obj.end_date < datetime.today().date()
        return False
    active_date.short_description = u'Expirou?'
    active_date.boolean = True

    def has_add_permission(self, request):
        return False


class VoucherAdmin(admin.ModelAdmin):
    list_display = ('promotion', 'cpf', )


admin.site.register(Promotion, PromotionAdmin)
# admin.site.register(Voucher, VoucherAdmin)
