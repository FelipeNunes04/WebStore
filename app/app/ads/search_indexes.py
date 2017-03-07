# coding: utf-8
from haystack.indexes import *
from haystack import site
from models import Ad


class AdIndex(SearchIndex):
    fancy_name = CharField(document=True, use_template=True, )
    description = CharField(model_attr='description', )
    category = CharField(model_attr='category', )
    site = CharField(model_attr='site', )
    city = CharField(model_attr='city', )
    zip_code = CharField(model_attr='zip_code', )
    street = CharField(model_attr='street', )
    area = CharField(model_attr='area', )
    number = CharField(model_attr='number', )
    country = CharField(model_attr='country', )
    time_working = CharField(model_attr='time_working', )
    type_ad = CharField(model_attr='type_ad', )
    activities = MultiValueField()
    option_values = MultiValueField()
    payment = MultiValueField()
    is_national = CharField()

    def index_queryset(self):
        """Used when the entire index for model is updated."""
        return Ad.active.all()

    # def prepare_area(self, obj):
    #     return [area.id for area in obj.area.all()]

    def prepare_activities(self, obj):
        return [activity.id for activity in obj.activities.all()]

    def prepare_option_values(self, obj):
        return [option_value.id for option_value in obj.option_values.all()]

    def prepare_payment(self, obj):
        return [payment.id for payment in obj.payment.all()]

    def prepare_is_national(self, obj):
        if obj.is_national:
            return 'sim'
        else:
            return 'nao'

site.register(Ad, AdIndex)
