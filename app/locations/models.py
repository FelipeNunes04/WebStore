# coding: utf-8
from django.contrib.localflavor.br.br_states import STATE_CHOICES
from django.db import models


class State(models.Model):
    state = models.CharField(u'estado', choices=STATE_CHOICES, max_length=2, )

    class Meta:
        verbose_name, verbose_name_plural = u'Estado', u'Estados'
        ordering = ('state', )

    def __unicode__(self):
        return self.state


class City(models.Model):
    city = models.CharField(u'cidade', max_length=64, )
    state = models.ForeignKey(State, verbose_name=u'estado')

    class Meta:
        verbose_name, verbose_name_plural = u'Cidade', u'Cidades'
        ordering = ('city', )

    def __unicode__(self):
        return self.city


class Area(models.Model):
    city = models.ForeignKey(City, verbose_name=u'cidade')
    area = models.CharField(u'bairro', max_length=64)

    class Meta:
        verbose_name, verbose_name_plural = u'Bairro', u'Bairros'
        ordering = ('area', )

    def __unicode__(self):
        return self.area


class ZipCode(models.Model):
    zip_code = models.CharField(u'cep', max_length=8, unique=True)
    city = models.ForeignKey(City, verbose_name=u'cidade')
    area = models.ForeignKey(Area, verbose_name=u'bairro')
    address = models.CharField(u'endereço', max_length=255)

    class Meta:
        verbose_name, verbose_name_plural = u'CEP', u'CEP'
        ordering = ('zip_code', )

    def __unicode__(self):
        return self.zip_code
