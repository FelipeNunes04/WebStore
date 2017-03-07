# coding: utf-8
from datetime import datetime, timedelta, date
from signals import moderate_comment, authorized_comment
from django.contrib.comments.models import Comment
from django.contrib.comments.moderation import CommentModerator, moderator
from django.contrib.comments.signals import comment_was_posted
from django.db import models
from django.db.models import signals
from django.template.defaultfilters import slugify
from category.models import Activity, Category, OptionValue
from customer.models import Advertiser
from locations.models import City, Area, State
from payment.models import Payment
import managers



class Plan(models.Model):
    name = models.CharField(u'plano', max_length=64)
    days = models.IntegerField(u'dias', help_text=u'Cadastrar o número de'
                                ' dias referente a quantidade de meses.')
    value_ad = models.DecimalField(u'valor primeiro anúncio',
                        decimal_places=2, max_digits=8, default=0, )
    # value_ad_extra = models.DecimalField(u'valor anúncios extras',
    #                     decimal_places=2, max_digits=8, default=0, )
    # value_banner = models.DecimalField(u'valor primeiro banner',
    #                     decimal_places=2, max_digits=8, default=0, )
    # value_banner_extra = models.DecimalField(u'valor de banners extras',
    #                     decimal_places=2, max_digits=8, default=0, )
    # value_photo_home = models.DecimalField(u'valor da foto no carroussel'
    #                     ' da home', decimal_places=2, max_digits=8,
    #                                                           default=0, )

    class Meta:
        verbose_name, verbose_name_plural = u'Plano', u'Planos'

    def __unicode__(self):
        return u'%s por R$%s ' % (self.name, self.value_ad, )


class Signature(models.Model):
    plan = models.ForeignKey(Plan, verbose_name=u'Plano', )
    customer = models.ForeignKey(Advertiser, verbose_name=u'Anunciante',)
    number_ads = models.IntegerField(u'número de anúncios', max_length=3,
                                    default=0, )
    # number_banners = models.IntegerField(u'número de banners', max_length=3,
    #                     default=0, )
    # number_carousel_home = models.IntegerField(u'carroussel', max_length=3,
    #   default=0, help_text='Quantidade de fotos no carroussel da home', )
    value_signature = models.DecimalField(
        u'Valor da assinatura', decimal_places=2, null=True, blank=True,
        max_digits=8, help_text='Deixe em branco para ser calculado'
        'automaticamente.', )
    number_ads_available = models.IntegerField(u'número de anúncios'
                            u' disponíveis', max_length=3, null=True,
                                                                blank=True, )
    # number_banners_available = models.IntegerField(u'número de banners'
    #               u' disponíveis', max_length=3, null=True, blank=True, )
    # number_carousel_home_available = models.IntegerField(u'carroussel',
    #                                     max_length=3, null=True, blank=True,
    #                                 help_text='Fotos do carroussel da home.')
    start_date = models.DateTimeField(u'data de início',
                                        default=datetime.now(),
        help_text='Esta data deve ser a de ativação da assinatura.')
    end_date = models.DateTimeField(u'data final', null=True, blank=True, )

    is_active = models.BooleanField(u'ativo', default=False, )
    objects = models.Manager()
    active = managers.ActiveSignatureManager()

    class Meta:
        verbose_name, verbose_name_plural = u'Assinatura', u'Assinaturas'

    def __unicode__(self):
        return u'%s - %s anúncios' % (self.customer, self.number_ads, )

    """
    Calcula o numero de anúncios, banners, e img do carroussel da home
    disponíveis por assinatura.
    """

    def calculate_ads_available(self):
        self.number_ads_available = (self.number_ads - self.ad_set.count())
        return self.number_ads_available

    """
    Calcula data final da assinatura
    """

    def signature_end(self):
        self.end_date = (self.start_date + timedelta(days=self.plan.days))
        return self.end_date

    def signature_inactive(self):
        self.is_active = False
        self.save()

    def signature_expired(self):
        now = datetime.now()
        if self.end_date <= now:
            return True
        return False

    # def calculate_banners_available(self):
    #     self.number_banners_available = (self.number_banners -
    #                                             self.banner_set.count())
    #     return self.number_banners_available
    #
    # def calculate_carousel_home_available(self):
    #     self.number_carousel_home_available = (self.number_carousel_home -
    #                                           self.carouselhome_set.count())
    #     return self.number_carousel_home_available

    """
    Calcula o valor da assinatura de acordo com o valor de cada,
    e seus extras com descontos, save comentado calcula a assinatura com todos
    itens.
    """

    # def save(self, *args, **kwargs):
    #     self.calculate_ads_available()
    #     self.calculate_banners_available()
    #     self.calculate_carousel_home_available()
    #     if not self.value_signature:
    #         self.value_signature = self.plan.value_ad+self.plan.value_banner\
    #                     + self.plan.value_photo_home\
    #                     + ((self.number_ads - 1) * self.plan.value_ad_extra)\
    #                     + ((self.number_banners - 1)
    #                     * self.plan.value_banner_extra)
    #     return super(Signature, self).save(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.calculate_ads_available()
        self.signature_end()
        if not self.value_signature:
            self.value_signature = self.plan.value_ad * self.number_ads
        return super(Signature, self).save(*args, **kwargs)


class Ad(models.Model):
    COMMERCE, SERVICE, EVENT = 'comercio', 'servico', 'evento'
    TYPE_AD_C = (
        (COMMERCE, u'Comércio'),
        (SERVICE, u'Serviço'),
        (EVENT, u'Evento'),
    )
    category = models.ForeignKey(Category, verbose_name='categoria', )
    signature = models.ForeignKey(Signature, verbose_name='assinatura', )
    user = models.ForeignKey(
                            Advertiser, verbose_name=u'Anunciante',
                help_text='Somente clientes cadastrados como anunciantes.',)
    type_ad = models.CharField(u'tipo de anúncio', max_length=64,
                                choices=TYPE_AD_C, )
    activities = models.ManyToManyField(Activity, verbose_name='atividade', )
    option_values = models.ManyToManyField(OptionValue,
                                            verbose_name='opções', )
    payment = models.ManyToManyField(Payment,
                                        verbose_name=u'forma de pagamento', )
    fancy_name = models.CharField(u'nome fantasia', max_length=64, )
    description = models.TextField(u'descrição', )
    image = models.ImageField(u'logo', upload_to='ads/logo/%Y/',
                                help_text='Tamanho da imagem 195x195.')
    video = models.CharField(u'vídeo', max_length=128,
                                help_text='ex. http://www.'
                                'youtube.com/watch?v=rWlHtvZHbZ'
                                ' ou http://www.vimeo.com/374627364',
                                blank=True, null=True, )
    site = models.URLField(u'site', null=True, blank=True,
                                verify_exists=False, )
    facebook = models.URLField(u'facebook', null=True, blank=True, )
    twitter = models.URLField(u'twitter', null=True, blank=True, )
    slug = models.SlugField(u'slug', max_length=64, unique=True, )
    time_working = models.TextField(u'horário de funcionamento', null=True,
                                    blank=True, )

    is_active = models.BooleanField(u'ativo', default=True, )

    objects = models.Manager()
    active = managers.ActiveAdManager()

    zip_code = models.CharField(u'CEP', max_length=9, )
    street = models.CharField(u'rua', max_length=256, )
    number = models.CharField(u'número', max_length=8, )
    complement = models.CharField(u'complemento', max_length=64,
                                    null=True, blank=True, )
    state = models.ForeignKey(State, verbose_name=u'estado', )
    city = models.ForeignKey(City, verbose_name='cidade', )
    area = models.ForeignKey(Area, verbose_name=u'bairro', null=True,
                                blank=True, )
    country = models.CharField(u'pais', max_length=128, null=True, blank=True,)
    is_national = models.BooleanField(u'exibição nacional', default=False)
    views = models.IntegerField(u'vizualizações do anúncio', default=0, )

    class Meta:
        verbose_name, verbose_name_plural = u'Anúncio', u'Anúncios'

    """
    Soma uma view ao video
    """

    def add_views(self):
        self.views += 1
        self.save()

    def __unicode__(self):
        return self.fancy_name

    def save(self, *args, **kwargs):
        ad = super(Ad, self).save(*args, **kwargs)
        self.signature.calculate_ads_available()
        self.signature.save()
        return ad

    def has_active_promotions(self):
        """
        Testa se existe alguma promoção ativa no anúncio e retorna True para
        o template de resultado de busca.
        """
        today = date.today()
        promotions = self.promotion_set.all()
        for p in promotions:
            if (p.is_active == True) and\
                ((not p.end_date) or (p.end_date >= today)) and \
                (p.start_date <= today) and (p.coupons < p.limit_vouchers):
                return True
        return False


class Photo(models.Model):
    ad = models.ForeignKey(Ad)
    name = models.CharField(u'nome', max_length=32, blank=True,
                    null=True, )
    description = models.CharField(u'descrição', max_length=64, blank=True,
                    null=True, )
    photo = models.ImageField(u'foto', upload_to='ads/photos/%Y/', )

    class Meta:
        verbose_name, verbose_name_plural = u'Foto', u'Fotos'

    def __unicode__(self):
        return self.name


def ad_pre_save(signal, instance, sender, **kwargs):
    if not instance.slug:
        slug = slugify(instance.fancy_name)
        new_slug = slug
        counter = 0

        while Ad.objects.filter(slug=new_slug).exclude(id=instance.id)\
                                                                .count() > 0:
            counter += 1
            new_slug = '%s-%d' % (slug, counter)

        instance.slug = new_slug

signals.pre_save.connect(ad_pre_save, sender=Ad)


class AdModerator(CommentModerator):
    email_notification = False

moderator.register(Ad, AdModerator)

signals.pre_save.connect(moderate_comment, sender=Comment)

comment_was_posted.connect(authorized_comment)
