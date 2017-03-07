# coding: utf-8
from datetime import datetime
from django.db import models
from django.db.models import Q


class ActiveEntryManager(models.Manager):
    """
    Queryset com os notícias ativas
    """

    def get_query_set(self, *args, **kwargs):
        now = datetime.now()
        return super(ActiveEntryManager, self)\
            .get_query_set(*args, **kwargs)\
            .filter(Q(date_expires__gte=now) | Q(date_expires__isnull=True))\
            .filter(Q(date_added__lte=now) | Q(date_added__isnull=True))