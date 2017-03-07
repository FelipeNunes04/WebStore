#coding: utf-8
from django.db import models


class Corporate(models.Model):
    superior_text = models.TextField(u'texto superior', )
    lower_text = models.TextField(u'texto inferior', )
    photo = models.ImageField(u'foto', upload_to='corporate/photos/%Y/',
                                        help_text='Tamanho: 346px x 210px', )
    video = models.CharField(u'vídeo', max_length=128,
                help_text='ex. http://www.youtube.com/watch?v=rWlHtvZHbZ'
                    ' ou http://www.vimeo.com/374627364', )

    class Meta:
        verbose_name, verbose_name_plural = u'Institucional', u'institucional'

    def __unicode__(self):
        return self.superior_text


class PrivacyPolicy(models.Model):
    text = models.TextField(u'texto', )

    class Meta:
        verbose_name, verbose_name_plural = u'Politica de privacidade',\
                                                    'Politica de privacidade'

    def __unicode__(self):
        return self.text


class TermsOfUse(models.Model):
    text = models.TextField(u'texto', )

    class Meta:
        verbose_name, verbose_name_plural = u'Termos de uso', u'Termos de uso'

    def __unicode__(self):
        return self.text
