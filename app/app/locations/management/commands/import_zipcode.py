import xlrd
from django.core.management.base import BaseCommand
from locations.models import City, Area, ZipCode


class Command(BaseCommand):

    def handle(self, *args, **options):
        wb = xlrd.open_workbook((args[0]), )
        sh = wb.sheet_by_index(0)
        # print sh.nrows
        for rownum in range(0, sh.nrows):
            zipc = str(int(sh.cell_value(rownum, 0)))
            if len(zipc) < 8:
                zipc = ('0%s') % int(sh.cell_value(rownum, 0))
            z = ZipCode(
                    zip_code=zipc,
                    address=sh.cell_value(rownum, 1),
                    city=City.objects.get(id=sh.cell_value(rownum, 2)),
                    area=Area.objects.get(id=sh.cell_value(rownum, 3)),
                )
            z.save()
            print '+1 - ', zipc
