# coding: utf-8
from datetime import datetime
from django.db import models
from category.models import Category
from locations.models import City
import  managers


class Banner(models.Model):
    category = models.ForeignKey(Category, verbose_name=u'categoria', )
    # signature = models.ForeignKey(Signature, verbose_name=u'assinatura', )
    name = models.CharField(u'nome do banner', max_length=64, )
    image = models.ImageField(u'imagem do banner', upload_to='banners/%Y/',
                                help_text='Tamanho da imagem 640px por 212px')
    link = models.URLField(u'link do anúncio', verify_exists=False, )
    city = models.ForeignKey(City)
    target = models.BooleanField(u'abrir em nova janela', default=False)
    date_added = models.DateTimeField(u'data de criação do banner',
                    default=datetime.now(), )
    start_date = models.DateTimeField(u'data de início do banner',
                     default=datetime.now(), )
    end_date = models.DateTimeField(u'data final do banner', )
    is_national = models.BooleanField(u'exibição nacional', default=False)
    is_active = models.BooleanField(u'ativo', default=False, )
    objects = models.Manager()
    active = managers.ActiveBannerManager()

    class Meta:
        verbose_name, verbose_name_plural = u'Banner', u'Banners'

    def __unicode__(self):
        return self.name

    # def banner_inactive(self):
    #     self.is_active = False
    #     self.save()

    # def banner_end(self):
    #     self.end_date = (self.start_date +
    #                             timedelta(days = self.signature.plan.days))
    #     return self.end_date

    # def save(self, *args, **kwargs):
    #     self.signature.calculate_banners_available()
    #     self.signature.save()
    #     self.banner_end()
    #     return super(Banner, self).save(*args, **kwargs)


class CarouselHome(models.Model):
    """
    Model do carroussel de destaque da home.
    """
    # signature = models.ForeignKey(Signature, verbose_name=u'assinatura', )
    name = models.CharField(u'nome', max_length=64, )
    img = models.ImageField(u'imagem',
                                upload_to='Fotos-carroussel-home/%Y/',
                                help_text='Tamanho da imagem 330x214.')
    link = models.URLField(u'link', verify_exists=False, )
    city = models.ForeignKey(City)
    target = models.BooleanField(u'abrir em nova janela', default=False, )
    date_added = models.DateTimeField(u'data de criação do banner',
                    default=datetime.now(), )
    start_date = models.DateTimeField(u'data de início do banner',
                     default=datetime.now(), )
    end_date = models.DateTimeField(u'data final do banner', )

    is_national = models.BooleanField(u'exibição nacional', default=False)
    is_active = models.BooleanField(u'ativo', default=False, )
    objects = models.Manager()
    active = managers.ActiveCarouselManager()

    class Meta:
        verbose_name_plural = u'Carroussel home'

    def __unicode__(self):
        return self.name

    # def carousel_end(self):
    #     self.end_date = (self.start_date +
    #                             timedelta(days = self.signature.plan.days))
    #     return self.end_date

    # def save(self, *args, **kwargs):
    #     self.signature.calculate_carousel_home_available()
    #     self.signature.save()
    #     self.carousel_end()
    #     return super(CarouselHome, self).save(*args, **kwargs)
