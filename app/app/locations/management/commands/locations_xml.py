# coding: utf-8
from xml.dom.minidom import parseString
from locations.models import City, Area, ZipCode
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        file = open('1_50000.xml', 'r')
        data = file.read()
        file.close()
        dom = parseString(data)

        for n in range(0, 4834147):
            xmlZipcode = dom.getElementsByTagName('cep')[n].toxml()
            xmlCity = dom.getElementsByTagName('id_cidade')[n].toxml()
            xmlArea = dom.getElementsByTagName('id_bairro')[n].toxml()
            xmlAddress = dom.getElementsByTagName('endereco')[n].toxml()

            zipcode = xmlZipcode.replace('<cep>', '').replace('</cep>', '')
            city = xmlCity.replace('<id_cidade>', '').\
                                    replace('</id_cidade>', '')
            area = xmlArea.replace('<id_bairro>', '').\
                                    replace('</id_bairro>', '')
            address = xmlAddress.replace('<endereco>', '').\
                                    replace('</endereco>', '')

            ZipCode.objects.create(
                zip_code=zipcode,
                city=City.objects.get(id=city),
                area=Area.objects.get(id=area),
                address=address
                )
            print '+1 - ',  zipcode
