# coding: utf-8
from django.template import Library
from category.models import Category

register = Library()


@register.inclusion_tag('menu.html')
def render_menu():
    menu = Category.objects.all().order_by('ordering')

    return {
        'menu': menu,
    }


@register.inclusion_tag('menu_footer.html')
def render_menu_footer():
    menu = Category.objects.all().order_by('ordering')

    return {
        'menu': menu,
    }
