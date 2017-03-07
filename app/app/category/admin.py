# coding: utf-8
from django.contrib import admin
from models import Activity, Category, OptionGroup, OptionValue


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'ordering', )
    prepopulated_fields = {
        'slug': ('name', )
    }
    search_fields = ('name', )

    class Media:
        js = ['js/jquery/jquery-1.4.2.min.js',
            'js/jquery/plugins/limit/jquery.limit-1.2.js',
            'admin/js/main.js']


class OptionValueAdmin(admin.TabularInline):
    extra = 0
    model = OptionValue
    prepopulated_fields = {
        'slug': ('name', )
    }


class OptionGroupAdmin(admin.ModelAdmin):
    inlines = [OptionValueAdmin]
    list_display = ('id', 'name', 'name_admin', 'slug', 'ordering', )
    list_display_links = ('name', 'name_admin', )
    list_filter = ('activity', )
    prepopulated_fields = {
        'slug': ('name', )
    }
    search_fields = ('id', 'name', 'name_admin', 'slug',)


class ActivityAdmin(admin.ModelAdmin):
    list_filter = ('categories', 'option_groups', )
    list_display = ('id', 'name', 'ordering', )
    list_display_links = ('id', 'name',)
    raw_id_fields = ('option_groups', )
    prepopulated_fields = {
        'slug': ('name', )
    }
    search_fields = ('name', )


# class OptionValueAdmin(admin.ModelAdmin):
#     list_display = ('id', 'name', )
#     search_fields = ('id', )

admin.site.register(Activity, ActivityAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(OptionGroup, OptionGroupAdmin)
# admin.site.register(OptionValue, OptionValueAdmin)
