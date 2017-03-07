# coding: utf-8
from django.template import Library
from django.db.models import Q
from polls.models import Question

register = Library()


@register.inclusion_tag('polls/poll.html', takes_context=True)
def render_poll(context):
    request = context['request']
    city = request.session.get('city')
    question = Question.active.all()
    if city:
        question = question.filter(Q(city=city, is_national=False) |
            Q(is_national=True))

    if question.exists():
        question = question.order_by('?')[0]
    else:
        question = None

    return {
        'question': question,
        }
