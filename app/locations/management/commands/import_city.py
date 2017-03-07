import xlrd
from django.core.management.base import BaseCommand
from locations.models import City, State


class Command(BaseCommand):

    def handle(self, *args, **options):
        wb = xlrd.open_workbook((args[0]), )
        sh = wb.sheet_by_index(0)
        # print sh.nrows
        for rownum in range(0, sh.nrows):
            c = City(
                id=sh.cell_value(rownum, 0),
                city=sh.cell_value(rownum, 1),
                state=State.objects.get(state=sh.cell_value(rownum, 2)),
                )
            c.save()
            print sh.cell_value(rownum, 1), '-', sh.cell_value(rownum, 2)
