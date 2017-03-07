# coding: utf-8
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.core.urlresolvers import reverse
from django.forms.models import model_to_dict
from django.shortcuts import redirect
from django.views.generic import FormView, TemplateView, UpdateView
from forms import (CustomerForm, EditRegistration, EditAdvertiserForm,
    AdvertiserForm, ForgotPasswordForm, CustomerToAdvertiserForm2,)
from ads.forms import ActiveAdForm
from ads.models import Signature, Ad


class CustomerFormView(FormView):
    template_name = 'customer/registration.html'
    form_class = CustomerForm

    def get_success_url(self):
        auth_user = authenticate(username=self.request.POST.get('email'),
            password=self.request.POST.get('password'))
        auth_login(self.request, auth_user)

        return reverse('success_registration')

    def form_valid(self, form):
        messages.success(self.request,
                    'Seu cadastro foi efetuado com sucesso.')
        form.save()
        return super(CustomerFormView, self).form_valid(form)


class SuccessRegistrationView(TemplateView):

    def get_template_names(self):
        if self.request.user.get_profile().is_advertiser:
            return 'customer/success_register_advertiser.html'
        return 'customer/success_registration.html'


class EditRegistrationView(UpdateView):

    def get_form_class(self):
        if self.request.user.get_profile().is_advertiser:
            return EditAdvertiserForm
        return EditRegistration

    def get_template_names(self):
        if self.request.user.get_profile().is_advertiser:
            return 'customer/edit_advertiser.html'
        return 'customer/edit_registration.html'

    def get_object(self, queryset=None):
        obj = self.request.user.get_profile().get_final_profile()
        return obj

    def get_success_url(self):
        return reverse('succes_edit_registration')


class SuccesEditRegistrationView(TemplateView):
    template_name = 'customer/success_edit_registration.html'


class AdvertiserFormView(FormView):
    template_name = 'customer/advertiser.html'

    def get_initial(self):
        if self.request.user.is_authenticated():
            instance = self.request.user.get_profile().get_final_profile()
            return model_to_dict(instance, fields=[field.name for field
                                                    in instance._meta.fields])
        return None

    def get_form_class(self):
        if self.request.user.is_authenticated() and\
            not self.request.user.get_profile().is_advertiser:
            return CustomerToAdvertiserForm2
        return AdvertiserForm

    def get_form_kwargs(self):
        kwargs = super(AdvertiserFormView, self).get_form_kwargs()
        if self.request.user.is_authenticated() and\
            not self.request.user.get_profile().is_advertiser:
            kwargs['user'] = self.request.user
        return kwargs

    def get_success_url(self):
        auth_user = authenticate(username=self.request.POST.get('email'),
            password=self.request.POST.get('password'))
        auth_login(self.request, auth_user)
        return reverse('success_registration')

    def form_valid(self, form):
        form.save()
        messages.success(self.request, u'Sua assinatura foi criada com'
                u' sucesso, aguarde e  você receberá o boleto para pagamento.')
        return super(AdvertiserFormView, self).form_valid(form)


class MyAdsFormView(FormView):
    template_name = 'customer/my_ads.html'
    form_class = ActiveAdForm

    def get_context_data(self, *args, **kwargs):
        context = super(MyAdsFormView, self).\
                    get_context_data(*args, **kwargs)
        context['list_my_signature'] = Signature.objects.\
                                    filter(customer__user=self.request.user)
        context['list_ads'] = Ad.objects.filter(user__user=self.request.user)

        return context


class ForgotPasswordView(FormView):
    form_class = ForgotPasswordForm
    template_name = 'customer/forgot_password.html'

    def form_valid(self, form, *args, **kwargs):
        form.save()

        messages.info(self.request, u'Uma nova senha foi enviada para'
                                                                'seu e-mail')

        next_url = self.request.GET.get('next')
        if next_url:
            return redirect('%s?next=%s' % (reverse('customer_signin'),
                                                        next_url))
        return redirect('customer_signin')
