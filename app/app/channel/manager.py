# coding: utf-8
from datetime import datetime
from django.db import models
from django.db.models import Q


class ActiveVideoManager(models.Manager):
    """
    Queryset com os vídeos ativos
    """

    def get_query_set(self, *args, **kwargs):
        now = datetime.now()
        return super(ActiveVideoManager, self)\
            .get_query_set(*args, **kwargs)\
            .filter(Q(date_expires__gte=now)|Q(date_expires__isnull=True))