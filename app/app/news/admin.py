# coding: utf-8
from django.contrib import admin
from models import Entry


class EntryAdmin(admin.ModelAdmin):
    list_display = ('title',  'category', 'date_added', 'date_expires',
                    'views', 'views_top', 'city', 'is_national', )
    list_filter = ('category', 'is_national',)
    prepopulated_fields = {
        'slug': ('title', ),
        }
    search_fields = ('title', )
    readonly_fields = ('views', )
    raw_id_fields = ('city', )
    search_fields = ('title', )
    # list_editable = ('title', 'views_top', 'date_added', )
    # list_display_links = ('category', )

    class Media:
        js = ['js/jquery/jquery-1.4.2.min.js',
             'js/jquery/plugins/limit/jquery.limit-1.2.js',
             'admin/js/main_new.js',
             'http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.2/jquery-ui.min.js',
             'http://yui.yahooapis.com/2.8.1/build/yahoo-dom-event/yahoo-dom-event.js',
             'http://yui.yahooapis.com/2.8.1/build/element/element-min.js',
             'http://yui.yahooapis.com/2.8.1/build/container/container_core-min.js',
             'http://yui.yahooapis.com/2.8.1/build/menu/menu-min.js',
             'http://yui.yahooapis.com/2.8.1/build/button/button-min.js',
             'http://yui.yahooapis.com/2.8.1/build/editor/editor-min.js',
             'http://yui.yahooapis.com/2.8.1/build/connection/connection-min.js',
             '/static/admin/js/table-editor.js',
             '/static/admin/js/yui_image_uploader.js',
             '/static/admin/js/yui.js', ]
        css = {
            'screen': ('http://yui.yahooapis.com/2.8.1/build/assets/skins/sam/skin.css',
                        '/static/admin/css/table-editor.css'),
        }


admin.site.register(Entry, EntryAdmin)
