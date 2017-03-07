# coding: utf-8
from django.contrib import admin
from models import Question, Choice, Vote


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 0
    readonly_fields = ('votes', )


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question', 'city', 'start_date', 'end_date',
                    'is_national', 'is_active', )
    fieldsets = [
        (None, {'fields': ['question', 'city', 'is_active', 'is_national', ]}),
        ('Datas', {'fields': ['date_added', 'start_date', 'end_date'],
            'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline, ]
    readonly_fields = ('date_added', )
    search_fields = ('title', )
    raw_id_fields = ('city', )


class VoteAdmin(admin.ModelAdmin):
    list_display = ('question', 'choice', 'ip', )

admin.site.register(Question, QuestionAdmin)
admin.site.register(Vote, VoteAdmin)
