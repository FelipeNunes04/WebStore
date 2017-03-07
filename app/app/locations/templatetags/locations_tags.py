# coding:utf-8
from django import template
from templatetag_sugar.register import tag
from templatetag_sugar.parser import Constant, Name
from ads.models import Ad
from locations.models import City

register = template.Library()


@tag(register, [Constant('as'), Name()])
def get_root_city(context, asvar):
    '''
    Usage {% get_root_city as [ var] %}
    '''
    context[asvar] = City.objects.all().order_by('city')
    return ''


@tag(register, [Constant('as'), Name()])
def get_root_city_ad(context, asvar):
    '''
    Usage {% get_root_city_ad as [ var] %}
    '''
    request = context['request']
    state = request.session['state']

    context[asvar] = Ad.active.filter(state=state).\
                        values('city', 'city__city', 'city__id').distinct()
    return ''


@tag(register, [Constant('as'), Name()])
def get_root_state(context, asvar):
    '''
    Usage {% get_root_state as [ var] %}
    '''
    context[asvar] = Ad.active.all().values('state', 'state__state')\
                                                .order_by('state').distinct()
    return ''
