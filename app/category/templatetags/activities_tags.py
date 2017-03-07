# coding:utf-8
from django import template
from templatetag_sugar.register import tag
from templatetag_sugar.parser import Constant, Name
from category.models import Category, OptionValue, Activity

register = template.Library()

@tag(register, [Constant('as'), Name()])
def get_root_category(context, asvar):
    ''' 
    Usage {% get_root_category as [ var] %}
    '''
    context [asvar] = Category.objects.all()
    return ''


@tag(register, [Constant('as'), Name()])
def get_root_option_value(context, asvar):
    ''' 
    Usage {% get_root_option_value as [ var] %}
    '''
    context [asvar] = OptionValue.objects.all()
    return ''


@tag(register, [Constant('as'), Name()])
def get_root_activity(context, asvar):
    ''' 
    Usage {% get_root_activity as [ var] %}
    '''
    context [asvar] = Activity.objects.all()
    return ''