# coding: utf-8
from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from wqti_util.email import EmailMessage
from django.contrib.comments.models import Comment


class SuggestionForm(forms.Form):
    suggestion = forms.CharField(label='Nome', )

    def save(self):
        message = EmailMessage(
            to=settings.CONTACT_EMAIL,
            subject=u'Não encontrado no site.',
            template='appsite/email/suggestion_email.txt',
            context=self.cleaned_data,
        )
        message.send()


class ReportForm(forms.Form):
    Subject_C = (
        ('Fora da categoria correta', u'Fora da categoria correta'),
        ('Racismo e/ou preconceito', u'Racismo e/ou preconceito'),
        ('Promove violencia e/ou atividade ilicitas', u'Promove violência e/ou atividade ilícitas'),
        ('Pornografia', u'Pornografia'),
        ('Improprio a menores de idade', u'Impróprio a menores de idade'),
        ('Viola meus direitos autorais', u'Viola meus direitos autorais'),
    )
    subject = forms.ChoiceField(label='Setor', choices=Subject_C, )
    name = forms.CharField(label='Nome', )
    email = forms.EmailField(label='E-mail', )
    message = forms.CharField(label='Mensagem',
                            widget=forms.widgets.Textarea(), required=False, )
    comment = forms.ModelChoiceField(queryset=Comment.objects.all(),\
                                    required=True, widget=forms.HiddenInput, )

    def save(self):
        message = EmailMessage(
        to=settings.CONTACT_EMAIL,
        subject=self.cleaned_data['subject'],
        template='appsite/email/report_email.txt',
        context= {'data': self.cleaned_data, 'comment': self.cleaned_data.get('comment')}
        )
        message.send()
