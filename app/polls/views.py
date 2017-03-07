# Create your views here.
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.views.generic import TemplateView
from models import Question, Choice, Vote


class PollView(TemplateView):
    """
    Mostra a enquete, e grava voto
    """
    template_name = 'polls/poll.html'

    def post(self, request, *args, **kwargs):
        question = get_object_or_404(Question, id=request.POST['question_id'])
        choice = get_object_or_404(Choice, id=request.POST['choice_id'],\
            question=question)

        if Vote.objects.filter(question=question, ip=request.META['REMOTE_ADDR']).exists():
            created = False
        else:
            Vote.objects.create(question=question, ip=request.META['REMOTE_ADDR'], choice=choice)
            created = True
            question.vote(choice)

        return HttpResponse(reverse('polls_result_view',\
            kwargs={'id': question.pk,
                'created': int(created)}))


class PollResultView(TemplateView):
    """
    Mostra o resultado da enquete
    """
    template_name = 'polls/poll_result.html'

    def get_context_data(self, **kwargs):
        context = super(PollResultView, self).get_context_data(**kwargs)
        context['question'] = Question.objects.get(id=self.kwargs['id'])
        context['created'] = self.kwargs['created']
        return context
