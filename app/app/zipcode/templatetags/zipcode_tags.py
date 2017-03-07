# coding:utf-8
from django import template
from templatetag_sugar.register import tag
from templatetag_sugar.parser import Constant, Name
from ads.models import Ad
from locations.models import ZipCode

register = template.Library()


@tag(register, [Constant('as'), Name()])
def get_root_state_zipcode(context, asvar):
    '''
    Usage {% get_root_state_zipcode as [ var] %}
    '''
    context[asvar] = ZipCode.objects.values('state').\
                        order_by('state').distinct()
    return ''
