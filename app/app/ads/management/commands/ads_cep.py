#coding: utf-8
from django.core.management.base import BaseCommand
from ads.models import Ad
from locations.models import State, City, Area


class Command(BaseCommand):

    def handle(self, *args, **options):
        for ad in Ad.objects.all():
            ad.city = City.objects.get(id=9560)
            ad.state = State.objects.get(id=3)
            ad.area = Area.objects.get(id=23280)
            ad.save()
            print 'Ad'
