#coding: utf-8
from django import forms
from django.forms import ModelForm
from models import Banner, CarouselHome


class AdminBannerForm(ModelForm):

    class Meta:
        model = Banner

    def clean(self):
        signature = self.cleaned_data.get('signature')

        if not self.instance.id and signature.calculate_banners_available() <= 0:
            raise forms.ValidationError('Confira o número de banners'
                                                ' disponíveis na assinatura.')
        return self.cleaned_data


class AdminCarouselHomeForm(ModelForm):

    class Meta:
        model = CarouselHome

    def clean(self):
        signature = self.cleaned_data.get('signature')

        if not self.instance.id and signature.calculate_carousel_home_available() <= 0:
            raise forms.ValidationError('Confira o número de foto-banners'
                                                ' disponíveis na assinatura.')
        return self.cleaned_data
