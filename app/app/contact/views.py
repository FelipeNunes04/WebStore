# coding: utf-8
from datetime import datetime
from django.conf import settings
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _
from django.views.generic import FormView
from forms import ContactForm
from polls.models import Question


class ContactFormView(FormView):
    template_name = 'contact/contact.html'
    form_class = ContactForm

    def get_success_url(self):
        return reverse('contact_form')

    def form_valid(self, form):
        form.save() #envia e-mail
        messages.success(self.request, 'Sua mensagem foi enviada com sucesso.'+
                        ' Aguarde e entraremos em contato.')
        return super(ContactFormView, self).form_valid(form)
