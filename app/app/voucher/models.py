#coding: utf-8
from django.db import models
from datetime import datetime, date
from ads.models import Ad
from customer.models import UserProfile
import managers


class Promotion(models.Model):
    TYPE_PROMOTION_C = (
        ('coupon', u'Cupom de desconto'),
        ('valley_toast', u'Vale brinde'),
    )
    type_promotion = models.CharField(u'tipo de promoção', max_length=20,
                                        choices=TYPE_PROMOTION_C, )
    ad = models.ForeignKey(Ad, verbose_name=u'anúncio', )
    title = models.CharField(u'título', max_length=128, )
    description = models.TextField(u'descrição', )
    start_date = models.DateField(u'data de início', default=datetime.now, )
    end_date = models.DateField(u'data final', null=True, blank=True, )
    image = models.ImageField(u'foto da promoção', upload_to='voucher/%Y/',
                                null=True, blank=True, )
    discount = models.DecimalField(u'desconto', max_digits=7, decimal_places=2,
                                    null=True, blank=True, )
    price = models.DecimalField(u'valor', max_digits=8, decimal_places=2,
                                null=True, blank=True, )
    discouted_price = models.DecimalField(u'preço com desconto', max_digits=8,
                                            decimal_places=2, null=True,
                                            blank=True, )
    limit_vouchers = models.IntegerField(u'limite de cupons', max_length=3, )
    coupons = models.IntegerField(u'cupons criados', max_length=3,
                                    help_text='Cupons já criados.', default=0,
                                    null=True, blank=True, )
    rules = models.TextField(u'regras', )
    is_active = models.BooleanField(u'cupom ativo', help_text='Desmarcar para'
                                    ' desativar cupom.', default=True, )
    objects = models.Manager()
    active = managers.ActivePromotionManager()

    class Meta:
        verbose_name, verbose_name_plural = u'Cupom', u'Cupons'
        ordering = ('-start_date', '-id')

    def __unicode__(self):
        return u'%s' % (self.title)

    def new_coupon(self):
        self.coupons += 1
        self.save()

    def limit_coupons(self):
        if self.coupons < self.limit_vouchers:
            return True
        return False

    def limit_date(self):
        if ((not self.end_date) or (self.end_date >= date.today())):
            return True
        return False

    def ad_signature_active(self):
        if (self.ad.is_active == True) and\
            (self.ad.signature.is_active == True):
            return True
        return False

    def promotion_active(self):
        now = date.today()
        if (self.is_active) and (self.start_date <= now) and\
            (self.coupons < self.limit_vouchers) and\
            ((not self.end_date) or (self.end_date >= now)):
            return True
        return False


class Voucher(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name=u'usuário', )
    promotion = models.ForeignKey(Promotion, verbose_name=u'promoção', )
    cpf = models.CharField(u'CPF', max_length=20, )
    code = models.CharField(u'código de validação', max_length=50,
                            unique=True, )

    class Meta:
        verbose_name, verbose_name_plural = u'cupom', u'cupons'

    def __unicode__(self):
        return u'%s - %s' % (self.promotion, self.code)
