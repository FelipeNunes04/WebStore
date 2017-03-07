#coding: utf-8
from datetime import datetime, timedelta
from optparse import make_option
from django.core.management.base import BaseCommand
from news.models import Entry


class Command(BaseCommand):

    def handle(self, *args, **options):
        now = datetime.now()
        for entry in Entry.objects.all():
            if (entry.date_added + timedelta(days = 7)) == now:
                entry.views_top = 0
                entry.save()
