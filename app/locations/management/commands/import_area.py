import xlrd
from django.core.management.base import BaseCommand
from locations.models import City, Area


class Command(BaseCommand):

    def handle(self, *args, **options):
        wb = xlrd.open_workbook((args[0]), )
        sh = wb.sheet_by_index(0)
        # print sh.nrows
        for rownum in range(0, sh.nrows):
            a = Area(
                    id=sh.cell_value(rownum, 0),
                    area=sh.cell_value(rownum, 1),
                    city=City.objects.get(id=sh.cell_value(rownum, 2)),
                )
            a.save()
            print sh.cell_value(rownum, 1)
