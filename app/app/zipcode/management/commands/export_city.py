#coding: utf-8
from optparse import make_option
from django.core.management.base import BaseCommand
from news.models import ZipCode
from locations.models import State, City, Area


class Command(BaseCommand):

    def handle(self, *args, **options):
        # objects = ZipCode.objects.all().values('state')
        # objects = objects.distinct()
        # for o in objects:
        #     s = State.objects.create(
        #         state=o['state'],
        #     )

        # city = ZipCode.objects.all().values('city', 'state').distinct().order_by('city')
        # for c in city:
        #     city = c['city']
        #     state = c['state']
        #     City.objects.create(
        #         city=city,
        #         state=State.objects.get(state=state)
        #     )

        area = ZipCode.objects.all().values('neighborhood', 'city', 'state').distinct().order_by('neighborhood')
        for a in area:
            area = a['neighborhood']
            city = a['city']
            state = a['state']
            Area.objects.create(
                area=area,
                city=City.objects.get(city=city, state__state=state)
            )