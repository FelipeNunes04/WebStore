# coding: utf-8
from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from wqti_util.email import EmailMessage


class ContactForm(forms.Form):
    Subject_C = (
        ('contato@virtuallia.com.br', u'Sugestão'),
        ('financeiro@virtuallia.com.br', u'Financeiro'),
        ('suporte@virtuallia.com.br', u'Suporte'),
        ('anuncie@virtuallia.com.br', u'Comercial - Banners'),
    )
    subject = forms.ChoiceField(label='Setor', choices=Subject_C, )
    name = forms.CharField(label='Nome', )
    email = forms.EmailField(label='E-mail', )
    phone = forms.CharField(label='Telefone', required=False, )
    city = forms.CharField(label='Cidade', )
    message = forms.CharField(label='Mensagem',
                            widget=forms.widgets.Textarea())

    def save(self):
        message = EmailMessage(
            to=self.cleaned_data['subject'],
            subject=u'Nova mensagem de contato postada no site.',
            template='contact/email.txt',
            context=self.cleaned_data,
        )
        message.send()
