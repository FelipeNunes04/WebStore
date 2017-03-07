#coding: utf-8
import uuid
from django import forms
from django.contrib.localflavor.br.forms import BRCPFField
from models import Promotion, Voucher
from ads.models import Ad
from customer.models import UserProfile


class PromotionForm(forms.ModelForm):

    class Meta:
        model = Promotion
        exclude = ('ad', 'coupons',)

    def __init__(self, ad, *args, **kwargs):
        super(PromotionForm, self).__init__(*args, **kwargs)
        self.ad = Ad.objects.get(slug=ad.slug)

    def clean(self):
        cleaned_data = super(PromotionForm, self).clean()
        type_promotion = cleaned_data.get('type_promotion')
        discount = cleaned_data.get('discount')
        price = cleaned_data.get('price')
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if end_date and start_date:
            if end_date < start_date:
                msg = u'não pode ser menor que data inicial.'
                self._errors['end_date'] = self.error_class([msg])
                del self.cleaned_data['end_date']
        if type_promotion == 'coupon':
            msg = 'Campo obrigatório para cupom de desconto.'
            if (discount == None):
                self._errors['discount'] = self.error_class([msg])
                del self.cleaned_data['discount']
            elif (price == None):
                self._errors['price'] = self.error_class([msg])
                del self.cleaned_data['price']
        return cleaned_data

    def save(self, *args, **kwargs):
        new_promotion = super(PromotionForm, self).save(commit=False,
                                                        *args, **kwargs)
        new_promotion.ad = Ad.objects.get(slug=self.ad.slug)
        new_promotion.save()
        return new_promotion


class NewVoucherForm(forms.ModelForm):
    cpf = BRCPFField(label=u'CPF')

    class Meta:
        model = Voucher
        exclude = ('user', 'promotion', 'code', )

    def new_code(self):
        code = uuid.uuid4()
        return code

    def __init__(self, promotion, user, *args, **kwargs):
        super(NewVoucherForm, self).__init__(*args, **kwargs)
        self.user = UserProfile.objects.get(email=user.email)
        self.promotion = Promotion.objects.get(pk=promotion.pk)

    def clean_cpf(self):
        cpf = self.cleaned_data.get('cpf')
        vouchers = Voucher.objects.filter(promotion=self.promotion.id)
        for v in vouchers:
            if cpf in v.cpf:
                raise forms.ValidationError(u'já cadastrado.')
        return cpf

    def save(self, *args, **kwargs):
        new_voucher = super(NewVoucherForm, self).save(commit=False,
                                                        *args, **kwargs)
        new_voucher.user = self.user
        new_voucher.code = self.new_code()
        new_voucher.promotion = Promotion.objects.get(pk=self.promotion.pk)
        new_voucher.save()
        return new_voucher
