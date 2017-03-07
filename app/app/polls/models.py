#coding: utf-8
from datetime import datetime
from django.db import models
from locations.models import City
import managers


class Question(models.Model):
    """
    Representa a pergunta da enquete
    """
    question = models.CharField(u'pergunta', max_length=128)
    city = models.ForeignKey(City, verbose_name=u'cidade', )
    date_added = models.DateTimeField(u'criado em',
                            default=datetime.now)
    start_date = models.DateTimeField(u'inicia em', null=True, blank=True)
    end_date = models.DateTimeField(u'termina em', null=True, blank=True)
    is_national = models.BooleanField(u'é nacional', default=False)

    is_active = models.BooleanField(u'ativo', default=True)
    objects = models.Manager()
    active = managers.ActiveQuestionManager()

    class Meta:
        verbose_name, verbose_name_plural = u'Questão', u'Questões'

    def __unicode__(self):
        return self.question

    def vote(self, choice):
        choice.votes += 1
        choice.save()


class Choice(models.Model):
    """
    Representa cada alternativa da enquete
    """
    question = models.ForeignKey(Question)
    choice = models.CharField(u'resposta', max_length=128)
    votes = models.IntegerField(u'votos', default=0)

    class Meta:
        verbose_name, verbose_name_plural = u'Resposta', u'Respostas'

    def __unicode__(self):
        return self.choice


class Vote(models.Model):
    '''
    Representa os votos
    '''

    question = models.ForeignKey(Question)
    choice = models.ForeignKey(Choice)
    ip = models.IPAddressField()

    class Meta:
        unique_together = ('question', 'ip')
