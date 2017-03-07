# coding: utf-8
from datetime import datetime
from django.db import models
from django.db.models import Q


class ActiveQuestionManager(models.Manager):
    """
    Queryset com as enquetes ativas (is_active=True e datas de
    início e fim válidas)
    """

    def get_query_set(self, *args, **kwargs):
        now = datetime.now()
        return super(ActiveQuestionManager, self).\
            get_query_set(*args, **kwargs).filter(is_active=True) \
                .filter(Q(end_date__gte=now) | Q(end_date__isnull=True)) \
                .filter(Q(start_date__lte=now) | Q(start_date__isnull=True))
