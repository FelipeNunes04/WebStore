# coding: utf-8
from datetime import datetime
from django.db import models
from category.models import Category
from locations.models import City
from manager import ActiveEntryManager


class Entry(models.Model):
    category = models.ForeignKey(Category)
    title = models.CharField(u'título', max_length=128)
    brief = models.TextField(u'resumo', max_length=90, blank=True, null=True,
                help_text=u'Máximo de 90 caracteres')
    city = models.ForeignKey(City)
    date_added = models.DateTimeField(u'data', default=datetime.now)
    text = models.TextField(u'conteúdo', help_text=u'A imagem não pode'
                                            u' ultrapassar 550px de largura.')
    img_display = models.ImageField(
                                    u'Imagem de exibição',
                                    upload_to='news/%Y/',
                                    help_text='Tamanho da imagem 210x165.')

    views = models.IntegerField(u'views em cada notícia', default=0, )
    date_expires = models.DateTimeField(u'data de expiração da notícia',
        null=True, blank=True,
        help_text=u'deixe em branco caso a notícia não expire')
    is_national = models.BooleanField(u'publicação nacional', default=False)
    views_top = models.IntegerField(u'views para contagem da home', default=0,
                        help_text=u'Essas views serão zeradas assim'
                                        u' que a notícia passar de 7 dias', )
    slug = models.SlugField(u'slug', unique=True, )

    objects = models.Manager()
    active = ActiveEntryManager()

    class Meta:
        verbose_name, verbose_name_plural = u'notícia', u'notícias'

    def __unicode__(self):
        return self.title

    def add_views(self):
        """
        Add uma view a notícia
        """
        self.views += 1
        self.views_top += 1
        self.save()
