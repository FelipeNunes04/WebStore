# coding: utf-8
import os
from django.db.models import Q
from django.views.generic import DetailView
from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from models import Entry
from uuid import uuid4
from wqti_util.json import to_json_response


class EntryDetailView(DetailView):
    template_name = 'news/news_detail.html'
    context_object_name = 'entry'
    model = Entry

    def get_context_data(self, *args, **kwargs):
        context = super(EntryDetailView, self).\
                    get_context_data(*args, **kwargs)
        city = self.request.session.get('city')
        qs_news_list = Entry.active.filter(category=self.object.category). \
            exclude(id=self.object.id).\
            order_by('-date_added')
        if city:
            qs_news_list = qs_news_list.filter(Q(city=city, is_national=False) | 
                Q(is_national=True))
        context['news_list'] = qs_news_list
        entry = context['entry']
        entry.add_views()
        return context
