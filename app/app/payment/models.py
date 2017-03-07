#coding: utf-8
from django.db import models

class Payment(models.Model):
    name = models.CharField(u'name', max_length=64, )
    slug = models.SlugField(u'slug', unique=True, )
    
    class Meta:
        verbose_name, verbose_name_plural = u'Forma de pagamento',\
                                                        u'Formas de pagamento'
        ordering = ('name', )

    def __unicode__(self):
        return self.name