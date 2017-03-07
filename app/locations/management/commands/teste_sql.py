import xlrd
from django.core.management.base import BaseCommand
from locations.models import City, State, Area, ZipCode


class Command(BaseCommand):

    def handle(self, *args, **options):