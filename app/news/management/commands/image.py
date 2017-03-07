#coding: utf-8
from optparse import make_option
from django.core.management.base import BaseCommand
from news.models import Entry


class Command(BaseCommand):

    def handle(self, *args, **options):
        for entry in Entry.objects.all():
            entry.img_display = entry.image
            entry.save()
