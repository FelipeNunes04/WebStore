#coding: utf-8
import csv
from django.core.management.base import BaseCommand
from zipcode.models import ZipCode


class Command(BaseCommand):

    def handle(self, *args, **options):
        csvreader = csv.reader(open(args[0]), delimiter='|', )
        for row in csvreader:
            o = ZipCode(
                zip_code=row[0],
                address=row[1],
                neighborhood=row[2],
                city=row[3],
                state=row[4],
            )
            o.save()
