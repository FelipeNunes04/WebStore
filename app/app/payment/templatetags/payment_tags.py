# coding:utf-8
from django import template
from templatetag_sugar.register import tag
from templatetag_sugar.parser import Constant, Name, Optional, Variable
from payment.models import Payment

register = template.Library()

@tag(register, [Constant('as'), Name(), Optional([Constant("for"), Variable()])])
def get_root_payment(context, asvar, ads=None):
    ''' 
    Usage {% get_root_payment as [ var] for [ list_ads ] %}
    '''
    if ads:
        payments = ads.values('payment')
        context[asvar] = Payment.objects.filter(pk__in=payments)
    else:
        context[asvar] = Payment.objects.all().order_by('name')
    return ''