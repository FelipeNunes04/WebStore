# coding: utf-8
import os
import re
from django import forms
from django.conf import settings
from django.core.urlresolvers import reverse
from django.forms import ModelForm
from django.forms.models import inlineformset_factory
from django.forms.widgets import CheckboxSelectMultiple, RadioSelect
from wqti_util.email import EmailMessage
from locations.models import City, Area, ZipCode
from category.models import Activity, Category, OptionValue
from models import Ad, Photo, Signature
from payment.models import Payment


class AdContactForm(forms.Form):
    name = forms.CharField(label='Nome', )
    email = forms.EmailField(label='E-mail', )
    phone = forms.CharField(label='Telefone', required=False, )
    city = forms.CharField(label='Cidade', )
    message = forms.CharField(label='Mensagem',
                    widget=forms.widgets.Textarea())

    def save(self, slug):
        ad = Ad.objects.get(slug=slug)
        message = EmailMessage(
            to=ad.user.email,
            subject='Contato do site Virtuallia',
            template='ads/email.txt',
            context=self.cleaned_data,
        )

        message.send()


class AdIndicateForm(forms.Form):
    my_name = forms.CharField(label='Seu nome', )
    my_email = forms.EmailField(label='Seu email', )
    friend_name = forms.CharField(label='Nome do seu amigo', )
    friend_email = forms.EmailField(label='Email do seu amigo', )

    def save(self, slug):
        ad = Ad.objects.get(slug=slug)
        url = reverse('ads_detail_view', kwargs={'slug': ad.slug})
        message = EmailMessage(
            to=self.cleaned_data['friend_email'],
            subject='Contato do site Virtuallia',
            template='ads/indicate.txt',
            context={
                'instance': self.cleaned_data, 'ad': ad, 'url': url,
                })
        message.send()


class AdminEditAdForm(ModelForm):

    class Meta:
        model = Ad

    def clean(self):
        signature = self.cleaned_data.get('signature')
        if not self.instance.id and signature.calculate_ads_available() <= 0:
            raise forms.ValidationError('Confira o número de anúncios'
                                                ' disponíveis na assinatura.')
        return self.cleaned_data

    def __init__(self, *args, **kwargs):
        super(AdminEditAdForm, self).__init__(*args, **kwargs)
        self.fields['state'].choices = [(i['state'], i['state'])\
                        for i in City.objects.values('state').distinct()]


class EditAdForm(ModelForm):
    category = forms.ModelChoiceField(required=True, empty_label=None,
                        widget=RadioSelect, queryset=Category.objects.all(),
                                                        label=u'Categoria')
    activities = forms.ModelChoiceField(required=True,
                        widget=RadioSelect, queryset=Activity.objects.all(),
                                                            label=u'Seções')
    option_values = forms.ModelMultipleChoiceField(required=True,
                                            widget=CheckboxSelectMultiple,
                queryset=OptionValue.objects.all(), label='Características')
    payment = forms.ModelMultipleChoiceField(required=True,
                                                widget=CheckboxSelectMultiple,
                queryset=Payment.objects.all(), label=u'Formas de pagamento')
    city = forms.CharField(label=u'Cidade',
                    widget=forms.TextInput(attrs={'placeholder': 'Cidade *'}))
    area = forms.CharField(label=u'Bairro',
                    widget=forms.TextInput(attrs={'placeholder': 'Bairro *'}))

    class Meta:
        model = Ad
        fields = ('fancy_name', 'description', 'site', 'facebook', 'twitter',
                    'facebook', 'twitter', 'time_working', 'image',
                    'zip_code', 'street', 'number', 'complement', 'area',
                    'state', 'city', 'country', 'activities', 'payment',
                    'category', 'option_values', 'type_ad', )

    def __init__(self, *args, **kwargs):
        super(EditAdForm, self).__init__(*args, **kwargs)
        self.fields['state'].choices = [(i['state'], i['state'])\
                        for i in City.objects.values('state').distinct()]

    def clean(self):
        area = self.cleaned_data.get('area')
        city = self.cleaned_data.get('city')
        state = self.cleaned_data.get('state')
        zip_code = self.cleaned_data.get('zip_code')
        msg = u'Este campo é obrigatório.'

        if state != None:
            if city:
                if not City.objects.filter(city=city, state=state).exists():
                    self.cleaned_data['city'] = City.objects.create(
                                            city=city,
                                            state=state,
                                            )
                    message = EmailMessage(
                        to=settings.DEFAULT_TO_EMAIL,
                        subject='Nova cidade cadastrada',
                        template='ads/email/new_city.txt',
                        context={'cleaned_data': self.cleaned_data, },
                    )
                    message.send()
                else:
                    self.cleaned_data['city'] = City.objects.get(city=city,
                                                            state=state)
            else:
                self._errors['city'] = self.error_class([msg])
                del self.cleaned_data['city']

            try:
                city_new = City.objects.get(city=city, state=state)
            except forms.ValidationError:
                self._errors['city'] = self.error_class([msg])
                del self.cleaned_data['city']

            if area:
                if not Area.objects.filter(area=area, city=city_new).exists():
                    self.cleaned_data['area'] = Area.objects.create(
                                            area=area,
                                            city=City.objects.get(city=city,
                                                                state=state),
                                            )
                    message = EmailMessage(
                        to=settings.DEFAULT_TO_EMAIL,
                        subject='Novo bairro cadastrado',
                        template='ads/email/new_area.txt',
                        context={'cleaned_data': self.cleaned_data, },
                    )
                    message.send()
                else:
                    self.cleaned_data['area'] = Area.objects.get(area=area,
                                                            city=city_new)
            else:
                self._errors['area'] = self.error_class([msg])

            if zip_code:
                zip_code = re.sub('-', '', zip_code)
                if not ZipCode.objects.filter(zip_code=zip_code).exists():
                    new_city = City.objects.get(city=city, state=state)
                    ZipCode.objects.create(
                        zip_code=zip_code,
                        city=new_city,
                        area=Area.objects.get(area=area, city=new_city),
                        address=self.cleaned_data.get('street'),
                        )
                    message = EmailMessage(
                        to=settings.DEFAULT_TO_EMAIL,
                        subject='Novo CEP cadastrado',
                        template='ads/email/new_zip_code.txt',
                        context={'cleaned_data': self.cleaned_data, }
                        )
                    message.send()
            else:
                self.cleaned_data['zip_code'] = self.error_class([msg])
        else:
            self._errors['state'] = self.error_class([msg])
            self._errors['city'] = self.error_class(u'não cadastrada, '
                                u'selecione o ESTADO para cadastrar a cidade.')
            self._errors['area'] = self.error_class(u'não cadastrado, '
                                u'selecione o ESTADO para cadastrar o bairro.')
            # del self.cleaned_data['city']
            del self.cleaned_data['area']

        return self.cleaned_data

    def clean_image(self):
        image = self.cleaned_data.get('image', False)
        if image:
            if image.size > 200 * 1024:
                raise forms.ValidationError(u'Imagem maior que 200kb')
            return image
        else:
            raise forms.ValidationError(u'Não foi possivel ler imagem'
                                                                ' carregada')
        return self.cleaned_data

    def clean_activities(self):
        '''
         O cliente solicitou que no front aceitar somente uma opção, para
        atividade
        '''
        activities = self.cleaned_data.get('activities')
        return [activities]


class ActiveAdForm(ModelForm):

    class Meta:
        model = Ad
        fields = ('is_active', )


class EditImageAdForm(ModelForm):

    class Meta:
        model = Ad
        fields = ('image', )


class EditVideoAdForm(ModelForm):

    class Meta:
        model = Ad
        fields = ('video', )


class HiddenForm(ModelForm):
    photo = forms.CharField(widget=forms.HiddenInput)

    class Meta:
        model = Photo

PhotoFormSet = inlineformset_factory(Ad, Photo, max_num=6, extra=6,
                                                            can_delete=True)
PhotoHiddenFormSet = inlineformset_factory(Ad, Photo, form=HiddenForm,
                                                        max_num=6, extra=6)


class SignatureForm(ModelForm):

    class Meta:
        model = Signature
        exclude = ('customer', 'start_date')

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(SignatureForm, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        signature = super(SignatureForm, self).save(commit=False,
            *args, **kwargs)
        signature.customer = self.user.get_profile().get_final_profile()
        signature.save()
        message = EmailMessage(
            to=settings.FINANCIAL_EMAIL,
            subject='Nova assinatura',
            template='ads/new_signature.txt',
            context={'signature': signature},
        )
        message.send()

        message_advertiser = EmailMessage(
            to=signature.customer.email,
            subject='Nova assinatura no Virtuallia',
            template='ads/new_signature_advertiser.txt',
            context={'signature': signature},
        )
        message_advertiser.send()

        return signature


class NewAdForm(ModelForm):
    category = forms.ModelChoiceField(
        required=True, empty_label=None, label=u'Categoria',
        widget=RadioSelect, queryset=Category.objects.all(), )
    activities = forms.ModelChoiceField(
        required=True, widget=RadioSelect, queryset=Activity.objects.all(),
        label=u'Seções', )
    option_values = forms.ModelMultipleChoiceField(
        required=True, widget=CheckboxSelectMultiple, label='Características',
        queryset=OptionValue.objects.all(), )
    payment = forms.ModelMultipleChoiceField(
        required=True, widget=CheckboxSelectMultiple,
        queryset=Payment.objects.all(), label=u'Formas de pagamento', )
    image = forms.CharField(widget=forms.HiddenInput, label=u'Logo')
    video = forms.CharField(required=False, widget=forms.HiddenInput)
    city = forms.CharField(label=u'Cidade',
                    widget=forms.TextInput(attrs={'placeholder': 'Cidade *'}))
    area = forms.CharField(label=u'Bairro',
                    widget=forms.TextInput(attrs={'placeholder': 'Bairro *'}))

    class Meta:
        model = Ad
        exclude = ('user', 'slug', 'views', )

    def __init__(self, user, signature, *args, **kwargs):
        super(NewAdForm, self).__init__(*args, **kwargs)
        self.user = user
        self.fields['signature'].queryset = Signature.objects.\
                                                        filter(pk=signature)
        self.fields['signature'].empty_label = None
        self.fields['state'].empty_label = 'Estado *'
        self.fields['city'].empty_label = 'Cidade *'
        self.fields['area'].empty_label = 'Bairro *'

    def clean(self):
        area = self.cleaned_data.get('area')
        city = self.cleaned_data.get('city')
        state = self.cleaned_data.get('state')
        zip_code = self.cleaned_data.get('zip_code')
        msg = u'Este campo é obrigatório.'

        if state != None:
            if city:
                if not City.objects.filter(city=city, state=state).exists():
                    self.cleaned_data['city'] = City.objects.create(
                                            city=city,
                                            state=state,
                                            )
                    message = EmailMessage(
                        to=settings.DEFAULT_TO_EMAIL,
                        subject='Nova cidade cadastrada',
                        template='ads/email/new_city.txt',
                        context={'cleaned_data': self.cleaned_data, },
                    )
                    message.send()
                else:
                    self.cleaned_data['city'] = City.objects.get(city=city,
                                                            state=state)
            else:
                self._errors['city'] = self.error_class([msg])
                del self.cleaned_data['city']

            try:
                city_new = City.objects.get(city=city, state=state)
            except forms.ValidationError:
                self._errors['city'] = self.error_class([msg])
                del self.cleaned_data['city']

            if area:
                if not Area.objects.filter(area=area, city=city_new).exists():
                    self.cleaned_data['area'] = Area.objects.create(
                                            area=area,
                                            city=City.objects.get(city=city,
                                                                state=state),
                                            )
                    message = EmailMessage(
                        to=settings.DEFAULT_TO_EMAIL,
                        subject='Novo bairro cadastrado',
                        template='ads/email/new_area.txt',
                        context={'cleaned_data': self.cleaned_data, },
                    )
                    message.send()
                else:
                    self.cleaned_data['area'] = Area.objects.get(area=area,
                                                            city=city_new)
            else:
                self._errors['area'] = self.error_class([msg])

            if zip_code:
                zip_code = re.sub('-', '', zip_code)
                if not ZipCode.objects.filter(zip_code=zip_code).exists():
                    new_city = City.objects.get(city=city, state=state)
                    ZipCode.objects.create(
                        zip_code=zip_code,
                        city=new_city,
                        area=Area.objects.get(area=area, city=new_city),
                        address=self.cleaned_data.get('street'),
                        )
                    message = EmailMessage(
                        to=settings.DEFAULT_TO_EMAIL,
                        subject='Novo CEP cadastrado',
                        template='ads/email/new_zip_code.txt',
                        context={'cleaned_data': self.cleaned_data, }
                        )
                    message.send()
            else:
                self.cleaned_data['zip_code'] = self.error_class([msg])
        else:
            self._errors['state'] = self.error_class([msg])
            self._errors['city'] = self.error_class(u'não cadastrada, '
                                u'selecione o ESTADO para cadastrar a cidade.')
            self._errors['area'] = self.error_class(u'não cadastrada, '
                                u'selecione o ESTADO para cadastrar o bairro.')

        return self.cleaned_data

    def clean_signature(self):
        signature = self.cleaned_data.get('signature')
        if signature.calculate_ads_available() <= 0:
            raise forms.ValidationError(u'Todos anúncios dessa assinatura '
               u'estão sendo utilizados, favor escolher outra assinatura')
        return signature

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            filename = '%s%s%s' % (settings.PROJECT_PATH, '/media/', image)
            print filename
            if os.path.getsize(filename) > 200 * 1024:
                raise forms.ValidationError(u'Imagem maior que 200kb')
            return image
        else:
            raise forms.ValidationError(u'Não foi possivel ler imagem'
                                                                'carregada')

    def clean_activities(self):
        '''
        O cliente solicitou que no front aceitar somente uma opção, para
        atividade (seção no layout)
        '''
        activities = self.cleaned_data.get('activities')
        return [activities]

    def save(self, *args, **kwargs):
        new_ad = super(NewAdForm, self).save(commit=False, *args, **kwargs)

        new_ad.city = City.objects.get(city=self.cleaned_data.get('city'),
                                        state=self.cleaned_data.get('state'))
        new_ad.area = Area.objects.get(area=self.cleaned_data.get('area'),
                                        city=self.cleaned_data.get('city'))
        new_ad.user = self.user.get_profile().get_final_profile()
        new_ad.save()
        new_ad.activities = self.cleaned_data.get('activities')
        new_ad.option_values = self.cleaned_data.get('option_values')
        new_ad.payment = self.cleaned_data.get('payment')
        new_ad.save()
        return new_ad
