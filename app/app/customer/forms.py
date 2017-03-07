# coding: utf-8
from django import forms
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.localflavor.br.br_states import STATE_CHOICES
from django.forms import ModelForm
from django.forms.widgets import CheckboxSelectMultiple
from ads.models import Signature, Plan
from category.models import Category
from locations.models import State
from models import Customer, Advertiser, UserProfile
from wqti_util.email import EmailMessage


class CustomerForm(ModelForm):
    ''' cadastro de cliente '''
    birth_date = forms.DateField(required=True, label='Data de nascimento', )
    gender = forms.ChoiceField(choices=UserProfile.GENDER_C, required=True,
                                                                label='Sexo')
    password = forms.CharField(label=u'Senha', widget=forms.PasswordInput)
    check_password = forms.CharField(label=u'Confirmar senha',
                widget=forms.PasswordInput, )
    interest_area = forms.ModelMultipleChoiceField(required=False,
                                                widget=CheckboxSelectMultiple,
                                            queryset=Category.objects.all())

    class Meta:
        model = Customer
        exclude = ('user', 'advertiser', 'area_phone', 'phone',
                                        'area_cell_phone', 'cell_phone', )

    def __init__(self, *args, **kwargs):
        super(CustomerForm, self).__init__(*args, **kwargs)
        self.fields['gender'].empty_label = 'Sexo'

    def clean_image(self):
        image = self.cleaned_data.get('image', False)
        if image:
            if image.size > 200 * 1024:
                raise forms.ValidationError(u'Imagem maior que 200kb')
            return image
        else:
            pass
        return image

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(
                        Q(email__iexact=email) | Q(username__iexact=email)).\
                        exists():
            raise forms.ValidationError(u'Cliente com este e-mail já existe')

        return email

    def clean_check_password(self):
        password1 = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('check_password')
        if password1 != password2:
            raise forms.ValidationError(u'Senhas digitadas são diferentes.')
        if 3 > len(password1) or len(password1) > 12:
            raise forms.ValidationError(u'A senha deve conter no mínimo 3 e '
                                u'no máximo 12 de caracteres alfanuméricos.')
        return password2

    def save(self, *args, **kwargs):
        customer = super(CustomerForm, self).\
                        save(commit=False, *args, **kwargs)
        user = User.objects.create_user(
            username=self.cleaned_data.get('email'),
            email=self.cleaned_data.get('email'),
            password=self.cleaned_data.get('password'),
        )
        user.first_name = self.cleaned_data.get('name')
        user.last_name = self.cleaned_data.get('surname')
        user.is_staff = False
        user.is_active = True
        user.save()

        customer.user = user
        customer.save()

        # message = EmailMessage(
        #     to=self.cleaned_data['email'],
        #     subject='Cadastro no site Virtuallia',
        #     template='ads/indicate.txt',
        #     context={'instance': self.cleaned_data, 'ad': ad, 'url': url, }
        # )
        # message.send()

        return customer


class AdvertiserForm(forms.Form):
    plan = forms.ModelChoiceField(label=u'Plano', required=True,
                            empty_label=None, queryset=Plan.objects.all(), )
    number_ads = forms.IntegerField(label=u'Número de anúncios',
                                                            required=True, )
    value_signature = forms.CharField(label='Valor da assinatura', )

    name = forms.CharField(label=u'Nome / Razão social', required=True, )
    fancy_name = forms.CharField(label=u'Sobrenome / Nome fantasia',
                                                            required=True, )
    type_person = forms.ChoiceField(label=u'Tipo de cadastro', required=True,
                                                choices=Advertiser.PERSON_C, )
    cpf_cnpj = forms.CharField(label=u'CPF/CNPJ', required=True, )
    responsible = forms.CharField(label=u'Pessoa responsável',
                                                            required=False, )
    birth_date = forms.DateField(label=u'Data de nascimento', required=True, )
    gender = forms.ChoiceField(label=u'Sexo', required=True,
                                                choices=UserProfile.GENDER_C, )
    area_phone = forms.CharField(label=u'DDD telefone comercial',
                                    required=True, )
    phone = forms.CharField(label=u'Telefone comercial', required=True, )
    area_cell_phone = forms.CharField(required=False, )
    cell_phone = forms.CharField(label=u'Telefone celular', required=False, )
    image = forms.ImageField(label=u'Avatar', required=False, )
    zip_code = forms.CharField(label=u'CEP', required=True, )
    address = forms.CharField(label=u'Rua', required=True, )
    number = forms.CharField(label=u'Número', required=True, )
    complement = forms.CharField(label=u'Complemento', required=False, )
    area = forms.CharField(label=u'Bairro', required=True, )
    state = forms.ChoiceField(label=u'Estado', required=True,
                                                    choices=STATE_CHOICES, )
    city = forms.CharField(label=u'Cidade', required=True, )
    email = forms.EmailField(label=u'Email', required=True, )
    password = forms.CharField(label=u'Senha', required=True,
                                                widget=forms.PasswordInput, )
    check_password = forms.CharField(label=u'Confirmar senha', required=True,
                                                widget=forms.PasswordInput, )

    def __init__(self, *args, **kwargs):
        super(AdvertiserForm, self).__init__(*args, **kwargs)
        self.fields['type_person'].empty_label = '---------'

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(
                        Q(email__iexact=email) | Q(username__iexact=email)).\
                        exists():
            raise forms.ValidationError(u'Anunciante com este e-mail '
                                                                u'já existe')
        return email

    def clean_image(self):
        image = self.cleaned_data.get('image', False)
        if image:
            if image.size > 200 * 1024:
                raise forms.ValidationError(u'Imagem maior que 200kb')
            return image
        else:
            pass
        return image

    def clean_check_password(self):
        password1 = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('check_password')
        if password1 != password2:
            raise forms.ValidationError(u'Senhas digitadas são diferentes.')
        if 3 > len(password1) or len(password1) > 12:
            raise forms.ValidationError(u'A senha deve conter no mínimo 3 e'
                                u' no máximo 12 de caracteres alfanuméricos.')
        return password2

    def save(self):
        cleaned_data = self.cleaned_data
        u = User.objects.create_user(
            username=cleaned_data['email'],
            email=cleaned_data['email'],
            password=cleaned_data['password'],
        )
        a = Advertiser.objects.create(
            user=u,
            birth_date=cleaned_data['birth_date'],
            name=cleaned_data['name'],
            address=cleaned_data['address'],
            number=cleaned_data['number'],
            complement=cleaned_data['complement'],
            zip_code=cleaned_data['zip_code'],
            area=cleaned_data['area'],
            state=cleaned_data['state'],
            city=cleaned_data['city'],
            area_cell_phone=cleaned_data['area_cell_phone'],
            cell_phone=cleaned_data['cell_phone'],
            image=cleaned_data['image'],
            email=cleaned_data['email'],
            password=cleaned_data['password'],
            fancy_name=cleaned_data['fancy_name'],
            type_person=cleaned_data['type_person'],
            cpf_cnpj=cleaned_data['cpf_cnpj'],
            responsible=cleaned_data['responsible'],
            area_phone=cleaned_data['area_phone'],
            phone=cleaned_data['phone'],
            gender=cleaned_data['gender'],
        )

        plan = cleaned_data['plan']
        number_ads = cleaned_data['number_ads']
        value_signature = plan.value_ad * number_ads
        Signature.objects.create(
            customer=a,
            plan=cleaned_data['plan'],
            number_ads=cleaned_data['number_ads'],
            value_signature=value_signature,
        )
        message = EmailMessage(
            to=settings.CONTACT_EMAIL,
            subject='Quero ser anunciante.',
            template='customer/email/email_advertiser.txt',
            context=self.cleaned_data,
        )
        message.send()


class CustomerToAdvertiserForm2(forms.Form):
    plan = forms.ModelChoiceField(label=u'Plano', required=True,
                            empty_label=None, queryset=Plan.objects.all(), )
    number_ads = forms.IntegerField(label=u'Número de anúncios',
                                                            required=True, )
    value_signature = forms.CharField(label='Valor da assinatura', )
    name = forms.CharField(label=u'Nome / Razão social', required=True, )
    fancy_name = forms.CharField(label=u'Sobrenome / Nome fantasia',
                                                            required=True, )
    type_person = forms.ChoiceField(label=u'Tipo de cadastro', required=True,
                                                choices=Advertiser.PERSON_C, )
    cpf_cnpj = forms.CharField(label=u'CPF/CNPJ', required=True, )
    responsible = forms.CharField(label=u'Pessoa responsável',
                                                            required=False, )
    birth_date = forms.DateField(label=u'Data de nascimento', required=True, )
    gender = forms.ChoiceField(label=u'Sexo', required=True,
                                choices=UserProfile.GENDER_C, )
    area_phone = forms.CharField(label='DDD telefone comercial',
                                    required=True, )
    phone = forms.CharField(label=u'Telefone comercial', required=True, )
    area_cell_phone = forms.CharField(required=False, )
    cell_phone = forms.CharField(label=u'Telefone celular', required=False, )
    image = forms.ImageField(label=u'Avatar', required=False, )
    zip_code = forms.CharField(label=u'CEP', required=True, )
    address = forms.CharField(label=u'Rua', required=True, )
    number = forms.CharField(label=u'Número', required=True, )
    complement = forms.CharField(label=u'Complemento', required=False, )
    area = forms.CharField(label=u'Bairro', required=True, )
    state = forms.ChoiceField(label=u'Estado', required=True,
                                                    choices=STATE_CHOICES, )
    city = forms.CharField(label=u'Cidade', required=True, )

    email = forms.EmailField(label=u'Email', required=True, )
    password = forms.CharField(label=u'Senha', required=True,
                                                widget=forms.PasswordInput, )
    check_password = forms.CharField(label=u'Confirmar senha', required=True,
                                                widget=forms.PasswordInput, )

    def __init__(self, user, *args, **kwargs):
        super(CustomerToAdvertiserForm2, self).__init__(*args, **kwargs)
        self.user = user

    def clean_email(self):
        email = self.cleaned_data.get('email')
        user = self.user
        if user.username == email and user.email == email:
            return email
        elif User.objects.filter(
            Q(email__iexact=email) | Q(username__iexact=email)).exists():
            raise forms.ValidationError(u'Anunciante com este e-mail'
                                                                u' já existe.')
        return email

    def clean_cpf_cnpj(self):
        cpf_cnpj = self.cleaned_data.get('cpf_cnpj')
        if Advertiser.objects.filter(cpf_cnpj=cpf_cnpj).exists():
            raise forms.ValidationError(u'Anunciante com esse cpf/cnpj' +
                                                                u' já exite.')
        else:
            return cpf_cnpj

    def clean_image(self):
        image = self.cleaned_data.get('image', False)
        if image:
            if image.size > 200 * 1024:
                raise forms.ValidationError(u'Imagem maior que 200kb')
            return image
        else:
            pass
        return image

    def clean_check_password(self):
        password1 = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('check_password')
        if password1 != password2:
            raise forms.ValidationError(u'Senhas digitadas são diferentes.')
        if 3 > len(password1) or len(password1) > 12:
            raise forms.ValidationError(u'A senha deve conter no mínimo 3 e'
                                u' no máximo 12 de caracteres alfanuméricos.')
        return password2

    def save(self):
        cleaned_data = self.cleaned_data
        customer = self.user.get_profile().get_final_profile()
        self.user.first_name = self.cleaned_data.get('name')
        self.user.last_name = self.cleaned_data.get('fancy_name')
        self.user.save()
        customer.delete()
        a = Advertiser.objects.create(
            user=self.user,
            birth_date=cleaned_data['birth_date'],
            name=cleaned_data['name'],
            address=cleaned_data['address'],
            number=cleaned_data['number'],
            complement=cleaned_data['complement'],
            zip_code=cleaned_data['zip_code'],
            area=cleaned_data['area'],
            state=cleaned_data['state'],
            city=cleaned_data['city'],
            area_cell_phone=cleaned_data['area_cell_phone'],
            cell_phone=cleaned_data['cell_phone'],
            image=cleaned_data['image'],
            email=cleaned_data['email'],
            password=cleaned_data['password'],
            fancy_name=cleaned_data['fancy_name'],
            type_person=cleaned_data['type_person'],
            cpf_cnpj=cleaned_data['cpf_cnpj'],
            responsible=cleaned_data['responsible'],
            area_phone=cleaned_data['area_phone'],
            phone=cleaned_data['phone'],
        )

        plan = cleaned_data['plan']
        number_ads = cleaned_data['number_ads']
        value_signature = plan.value_ad * number_ads

        Signature.objects.create(
            customer=a,
            plan=cleaned_data['plan'],
            number_ads=cleaned_data['number_ads'],
            value_signature=value_signature,
        )
        message = EmailMessage(
            to=settings.CONTACT_EMAIL,
            subject='Quero ser anunciante.',
            template='customer/email/email_advertiser.txt',
            context=self.cleaned_data,
        )
        message.send()


class EditRegistration(ModelForm):
    birth_date = forms.DateField(required=False, label='Data de nascimento', )
    email = forms.EmailField(label=u'E-mail')
    password = forms.CharField(label=u'Senha', widget=forms.PasswordInput)
    password2 = forms.CharField(label=u'Confirmar senha',
                widget=forms.PasswordInput, )

    class Meta:
        model = Customer
        exclude = ('user', 'name', 'surname', )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        user = self.instance.user
        if user.username == email and user.email == email:
            return email
        elif User.objects.filter(
                        Q(email__iexact=email) | Q(username__iexact=email)).\
                        exists():
            raise forms.ValidationError(u'Cliente com este e-mail já existe')

        return email

    def clean_image(self):
        image = self.cleaned_data.get('image', False)
        if image:
            if image.size > 200 * 1024:
                raise forms.ValidationError(u'Imagem maior que 200kb')
            return image
        else:
            pass
        return image

    def clean_password2(self):
        password1 = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password1 != password2:
            raise forms.ValidationError(u'Senhas digitadas são diferentes.')
        if 3 > len(password1) or len(password1) > 12:
            raise forms.ValidationError(u'A senha deve conter no mínimo 3'
                            u' e no máximo 12 de caracteres alfanuméricos.')
        return password2

    def save(self, *args, **kwargs):
        customer = super(EditRegistration, self).save(*args, **kwargs)
        user = self.instance.user
        user.username = self.cleaned_data.get('email')
        user.email = self.cleaned_data.get('email')
        user.set_password = self.cleaned_data.get('password1')
        user.save()

        return customer


class EditAdvertiserForm(ModelForm):
    email = forms.EmailField(label=u'E-mail')
    password = forms.CharField(label=u'Senha', widget=forms.PasswordInput,
                                required=False)
    password2 = forms.CharField(label=u'Confirmar senha',
                widget=forms.PasswordInput, required=False)

    class Meta:
        model = Advertiser
        exclude = ('user', 'name', 'type_person', 'cpf_cnpj', 'fancy_name', )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        user = self.instance.user
        if user.username == email and user.email == email:
            return email
        elif User.objects.filter(
                        Q(email__iexact=email) | Q(username__iexact=email)).\
                        exists():
            raise forms.ValidationError(u'Cliente com este e-mail já existe')

        return email

    def clean_image(self):
        image = self.cleaned_data.get('image', False)
        if image:
            if image.size > 200 * 1024:
                raise forms.ValidationError(u'Imagem maior que 200kb')
            return image
        else:
            pass
        return image

    def clean_password2(self):
        password1 = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password1 != password2:
            raise forms.ValidationError(u'Senhas digitadas são diferentes.')
        if 3 > len(password1) or len(password1) > 12:
            raise forms.ValidationError(u'A senha deve conter no mínimo 3 e'
                                u' no máximo 12 de caracteres alfanuméricos.')
        return password2

    def save(self, *args, **kwargs):
        advertiser = super(EditAdvertiserForm, self).save(*args, **kwargs)
        user = self.instance.user
        user.username = self.cleaned_data.get('email')
        user.email = self.cleaned_data.get('email')
        if self.cleaned_data.get('password'):
            user.set_password = self.cleaned_data.get('password')
        user.save()

        return advertiser


class ForgotPasswordForm(forms.Form):
    email = forms.EmailField()

    def clean_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError(u'Este e-mail não está'
                                        u' cadastrado no sistema')
        return email

    def save(self):
        email = self.cleaned_data['email']
        user = User.objects.get(email=email)
        new_password = User.objects.make_random_password(length=8)
        user.set_password(new_password)
        user.save()

        msg = EmailMessage(
            to=[user.email],
            subject=u'Virtuallia - Sua nova senha de acesso',
            template='customer/email/forgot_password.txt',
            context={
                'user': user,
                'new_password': new_password,
            }
        )
        msg.send()
