# coding: utf-8
from datetime import datetime
from django.db import models
from django.db.models import F, Q


class ActivePromotionManager(models.Manager):
    """
    Queryset que retorna apenas as promoções ativas por data e
    pelo is_active
    """

    def get_query_set(self, *args, **kwargs):
        now = datetime.now()
        return super(ActivePromotionManager, self)\
                    .get_query_set(*args, **kwargs)\
                    .filter(is_active=True)\
                    .filter(Q(end_date__gte=now) | Q(end_date__isnull=True))\
                    .filter(start_date__lte=now)\
                    .filter(coupons__lt=F('limit_vouchers'))\
                    .filter(ad__is_active=True)\
                    .filter(ad__signature__is_active=True)\
                    .filter(ad__signature__end_date__gte=now)
