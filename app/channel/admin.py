# coding: utf-8
from django.contrib import admin
from models import Video


class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'date_added', 'date_expires',
                                            'views', 'city', 'is_national', )
    list_filter = ('category', 'is_national', )
    raw_id_fields = ('city', )
    readonly_fields = ('views', )
    prepopulated_fields = {'slug': ('title', )}
    search_fields = ('title', )
    fieldsets = [
        (None, {'fields': ['category', 'title', 'city', 'description',
                            'video', 'views', 'slug', 'is_national', ]}),
        ('Datas', {'fields': ['date_added', 'date_expires'],
            'classes': ['collapse']}),
        ]


admin.site.register(Video, VideoAdmin)
