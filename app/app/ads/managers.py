# coding: utf-8
from datetime import datetime
from django.db import models
from django.db.models import Q


class ActiveAdManager(models.Manager):
    """
    Queryset com os anúncios ativos (is_active=True e datas de
    início e fim do plano válidas)
    """

    def get_query_set(self, *args, **kwargs):
        now = datetime.now()
        return super(ActiveAdManager, self).\
            get_query_set(*args, **kwargs).filter(is_active=True) \
                .filter(signature__is_active=True)\
                .filter(signature__end_date__gte=now)


class ActiveSignatureManager(models.Manager):
    """
    Queryset que valida se assinatura esta ativa, de acordo com as datas.
    """

    def get_query_set(self, *args, **kwargs):
        now = datetime.now()
        return super(ActiveSignatureManager, self)\
            .get_query_set(*args, **kwargs).filter(is_active=True)\
            .filter(Q(end_date__gte=now) | Q(end_date__isnull=True))\
            .filter(Q(start_date__lte=now) | Q(start_date__isnull=True))
