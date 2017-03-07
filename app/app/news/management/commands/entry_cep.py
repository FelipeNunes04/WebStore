#coding: utf-8
from django.core.management.base import BaseCommand
from news.models import Entry
from locations.models import City
from channel.models import Video


class Command(BaseCommand):

    def handle(self, *args, **options):
        for entry in Entry.objects.all():
            entry.city = City.objects.get(id=9560)
            entry.is_national = True
            entry.save()
            print 'entry'

        for v in Video.objects.all():
            v.city = City.objects.get(id=9560)
            v.is_national = True
            v.save()
            print 'video'
