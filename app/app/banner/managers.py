# coding: utf-8
from datetime import datetime
from django.db import models
from django.db.models import Q


class ActiveBannerManager(models.Manager):
    """
    Queryset com o banner ativo (active=True) e datas de início e final,
    válidas (de acordo com o número de dias definido pela assinatura).
    """

    def get_query_set(self, *args, **kwargs):
        now = datetime.now()
        return super(ActiveBannerManager, self).\
            get_query_set(*args, **kwargs).filter(is_active=True)\
                .filter(Q(end_date__gte=now) | Q(end_date__isnull=True))\
                .filter(Q(start_date__lte=now) | Q(start_date__isnull=True))


class ActiveCarouselManager(models.Manager):
    """
    Queryset com foto carroussel da home ativa (active=True) e datas de início
    e final, válidas (de acordo com o número de dias definido pela
    assinatura).
    """

    def get_query_set(self, *args, **kwargs):
        now = datetime.now()
        return super(ActiveCarouselManager, self)\
            .get_query_set(*args, **kwargs).filter(is_active=True)\
                .filter(Q(end_date__gte=now) | Q(end_date__isnull=True))\
                .filter(Q(start_date__lte=now) | Q(start_date__isnull=True))
