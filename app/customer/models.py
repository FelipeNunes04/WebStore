# coding: utf-8
from django.contrib.auth.models import User
from django.db import models
from django.contrib.localflavor.br.br_states import STATE_CHOICES
from category.models import Category


class UserProfile(models.Model):
    ''' Classe que guarda od dados comuns entre os usúarios 'cliente' e
    'anunciante' '''

    MALE, FEMALE = 'male', 'female'
    GENDER_C = (
        (MALE, u'Masculino'),
        (FEMALE, u'Feminino'),
    )

    user = models.OneToOneField(User)
    birth_date = models.DateField(u'data de nascimento', null=True, blank=True)
    gender = models.CharField(u'sexo', max_length=16, choices=GENDER_C,
        null=True, blank=True)
    name = models.CharField(u'nome / razão social', max_length=256)
    address = models.CharField(u'endereço',
        max_length=128, blank=True, null=True, )
    number = models.CharField(u'número', max_length=16, blank=True, null=True)
    complement = models.CharField(u'complemento', max_length=32, null=True,
        blank=True, )
    city = models.CharField(u'cidade', max_length=64, blank=True, null=True, )
    area = models.CharField(u'bairro', max_length=64, blank=True, null=True, )
    state = models.CharField(u'estado', choices=STATE_CHOICES, max_length=2,
                                                    blank=True, null=True, )
    zip_code = models.CharField(u'CEP', max_length=9, blank=True, null=True, )
    is_advertiser = models.BooleanField(u'é anunciante', default=False, )
    email = models.EmailField(u'e-mail', )
    password = models.CharField(u'senha', blank=True, null=True,
                                max_length=128)
    area_cell_phone = models.CharField(u'ddd telefone celular', max_length=2,
        null=True, blank=True, )
    cell_phone = models.CharField(u'telefone celular', max_length=10,
        null=True, blank=True, )
    image = models.ImageField(u'avatar', upload_to="img/customer/",
        null=True, blank=True, )

    def get_final_profile(self):
        if self.is_advertiser:
            return Advertiser.objects.get(user__exact=self.user)
        return Customer.objects.get(user__exact=self.user)


class Customer(UserProfile):
    ''' usuário comum do site '''
    surname = models.CharField(u'sobrenome', max_length=128)
    area_phone = models.CharField(u'ddd telefone residencial',
        max_length=2, null=True, blank=True)
    phone = models.CharField(u'telefone residencial', max_length=10,
        null=True, blank=True)
    interest_area = models.ManyToManyField(Category,
        verbose_name=u'áreas de interesse', null=True, blank=True)
    newsletter = models.BooleanField(u'aceito receber e-mails', default=True, )

    class Meta:
        verbose_name, verbose_name_plural = u'cliente', u'clientes'

    def __unicode__(self):
        return u'%s %s - %s' % (self.user.first_name, self.user.last_name,
            self.user, )

    def save(self, *args, **kwargs):
        self.is_advertiser = False
        super(Customer, self).save(*args, **kwargs)


class Advertiser(UserProfile):
    ''' usuário anunciante '''
    INDIVIDUAL, LEGAL_ENTITY = 'individual', 'legal_entity'
    PERSON_C = (
        (INDIVIDUAL, u'Pessoa física'),
        (LEGAL_ENTITY, u'Pessoa juríca'),
    )
    fancy_name = models.CharField(u'nome fantasia', max_length=256)
    area_phone = models.CharField(u'ddd telefone comercial', max_length=2)
    phone = models.CharField(u'telefone comercial', max_length=10)
    type_person = models.CharField(u'tipo de cadastro', max_length=16,
        choices=PERSON_C, default='legal_entity')
    cpf_cnpj = models.CharField(u'CPF/CNPJ', max_length=20, unique=True)
    responsible = models.CharField(u'pessoa responsável', max_length=128)

    class Meta:
        verbose_name, verbose_name_plural = u'anunciante', u'anunciante'

    def __unicode__(self):
        return u'%s - %s' % (self.name, self.user)

    def save(self, *args, **kwargs):
        self.is_advertiser = True
        super(Advertiser, self).save(*args, **kwargs)
