#coding: utf-8
from datetime import datetime
from optparse import make_option
from django.core.management.base import BaseCommand
from ads.models import Signature


class Command(BaseCommand):

    def handle(self, *args, **options):
        now = datetime.now()
        for signature in Signature.objects.filter(end_date__lt=now):
            if signature.end_date < now:
                signature.signature_inactive()
