# coding: utf-8
from django.db import models


class Category(models.Model):
    name = models.CharField(u'nome', max_length=64, )
    description = models.TextField(u'breve descrição',
                                    help_text='Limite de caracteres: 350', )
    ordering = models.IntegerField(u'ordem', default=0, )
    slug = models.SlugField(u'slug', unique=True, )
    image_top_ten = models.ImageField(u'imagem top 11',
                    upload_to='ads/top-10/%Y/', help_text='Adicione uma '
                    'imagem de tamanho 252px de largura por 172px de altura ou'
                    u'maior nesta proporção.'
                    u' Essa imagem irá aparecer na seção top 11 da home.')

    class Meta:
        verbose_name, verbose_name_plural = u'Categoria', u'Categorias'

    def __unicode__(self):
        return self.name


class OptionGroup(models.Model):
    name = models.CharField(u'nome no site', max_length=128, )
    name_admin = models.CharField(u'nome no admin', max_length=64)
    ordering = models.IntegerField(u'ordem', default=0, )
    slug = models.SlugField(u'slug', unique=True, )

    class Meta:
        verbose_name, verbose_name_plural = u'Grupo de Opções',\
                                                        u'Grupo de Opções'
        ordering = ('name', )

    def __unicode__(self):
        return self.name_admin


class OptionValue(models.Model):
    option_group = models.ForeignKey(OptionGroup,
                                            verbose_name=u'opções', )
    name = models.CharField(u'name', max_length=64, )
    ordering = models.IntegerField(u'ordem', default=0, )
    slug = models.SlugField(u'slug', unique=True, )

    class Meta:
        verbose_name, verbose_name_plural = u'Opção', u'Opções'
        ordering = ('name', )

    def __unicode__(self):
        return self.name


class Activity(models.Model):
    categories = models.ManyToManyField(Category, verbose_name='categorias', )
    option_groups = models.ManyToManyField(OptionGroup,
                                            verbose_name=u'grupo de opções')
    name = models.CharField(u'name', max_length=64, )
    ordering = models.IntegerField(u'ordem', default=0, )
    slug = models.SlugField(u'slug', unique=True, )

    class Meta:
        verbose_name, verbose_name_plural = u'Atividade', u'Atividades'
        ordering = ('name', )

    def __unicode__(self):
        return self.name
