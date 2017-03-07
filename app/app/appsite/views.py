# coding: utf-8
import os
from datetime import datetime, timedelta
from uuid import uuid4
from django.conf import settings
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.comments.models import Comment
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.generic import TemplateView, FormView
from django.views.generic.simple import direct_to_template
from forms import SuggestionForm, ReportForm
from haystack.query import SearchQuerySet
from ads.models import Ad
from appsite.models import Corporate, PrivacyPolicy, TermsOfUse
from banner.models import Banner, CarouselHome
from channel.models import Video
from category.models import Category
from locations.models import Area
from news.models import Entry
from voucher.models import Promotion


class HomeTemplateView(TemplateView):
    """
    View para popular a home
    """
    template_name = 'appsite/home.html'

    def get_context_data(self, *args, **kwargs):
        context = super(HomeTemplateView, self).\
                    get_context_data(*args, **kwargs)
        city = self.request.session.get('city')
        qs_news = Entry.active
        qs_last_videos = Video.active.order_by('?', '-date_added')
        qs_top_ten = Ad.active.all()
        qs_carousel_home = CarouselHome.active.order_by('?')

        qs_promotions = Promotion.active.order_by('?')

        if city:
            qs_news = qs_news.filter(Q(city=city, is_national=False) |
                                Q(is_national=True))
            qs_last_videos = qs_last_videos.\
                                filter(Q(city=city, is_national=False) |
                                Q(is_national=True))
            qs_top_ten = qs_top_ten.filter(Q(city=city, is_national=False) |
                Q(is_national=True))
            qs_carousel_home = qs_carousel_home.\
                                filter(Q(city=city, is_national=False) |
                                Q(is_national=True))

        categories = Category.objects.order_by('?')
        list_top_ten = []
        for category in categories:
            if qs_top_ten.filter(category=category).exists():
                list_top_ten.append(qs_top_ten.filter(category=category)\
                    .order_by('-views')[0])

        '''
        últimas notícias, aparecer somente até 2 dias de cadastro
        '''
        last_news = qs_news.exclude(
                    date_added__lt=datetime.now() - timedelta(days=2))
        last_news = last_news.order_by('?')[:5]

        '''
        last_news, se não existir a lista pega em ordem aleatória
        outras 5 dicas.
        '''
        if last_news:
            last_news = last_news
        else:
            last_news = qs_news.all().order_by('?')[:5]

        '''
        Mostrar as 8 mais clicadas de acordo com o contador(views_top),
        excluindo as que repetem na last_news,
        e com no máximo com 7 dias da data de criação.
        '''
        news_top = qs_news.exclude(pk__in=[e.pk for e in last_news])\
                    .exclude(date_added__lt=datetime.now() - timedelta(days=7))
        news_top = news_top.order_by('?', '-views_top')

        '''
        news_top, se não existir a lista pega outras 4 notícias mais vistas em
        todo tempo do site, e coloca em oredem aleatória
        (excluindo as do last_news)
        '''
        if news_top:
            news_top = news_top
        else:
            news_top = qs_news.exclude(pk__in=[e.pk for e in last_news])\
                        .order_by('?', '-views')

        '''
        Verifica se existe ao menos 1 promoção para retornar o número correto
        de dicas
        '''
        if qs_promotions:
            news_top = news_top[:4]
        else:
            news_top = news_top[:8]

        for i in Promotion.active.all():
            i.ad_signature_active()

        context['last_news'] = last_news
        context['news_more_views'] = news_top
        context['last_videos'] = qs_last_videos[:5]
        context['top_ten'] = list_top_ten
        context['carousel_home'] = qs_carousel_home[:5]
        context['qs_promotions'] = qs_promotions[:4]
        return context


@staff_member_required
def image_upload(request):
    """
    Fazer upload de imagem
    """
    try:
        upload_full_path = '%scontent/images/' % settings.MEDIA_ROOT

        upload = request.FILES['image']
        filename = '%s.%s' % (uuid4(), upload.name.split('.')[-1])
        dest = open(os.path.join(upload_full_path, filename), 'wb+')

        for chunk in upload.chunks():
            dest.write(chunk)
        dest.close()

        result = '{status:"UPLOADED", image_url:"%s"}' %\
            ('%scontent/images/%s' % (settings.MEDIA_URL, filename))

        return HttpResponse(result, mimetype='text/html')

    except Exception:
        return HttpResponse("error")


class CorporateTemplateView(TemplateView):
    template_name = 'appsite/corporate.html'

    def get_context_data(self, **kwargs):
        context = super(CorporateTemplateView, self).get_context_data(**kwargs)

        context['corporate'] = Corporate.objects.all()[0]
        return context


class PrivacyTemplateView(TemplateView):
    template_name = 'appsite/privacy_policy.html'

    def get_context_data(self, **kwargs):
        context = super(PrivacyTemplateView, self).get_context_data(**kwargs)

        context['privacy'] = PrivacyPolicy.objects.all()[0]
        return context


class TermsOfUseTemplateView(TemplateView):
    template_name = 'appsite/terms_of_use.html'

    def get_context_data(self, **kwargs):
        context = super(TermsOfUseTemplateView, self)\
                    .get_context_data(**kwargs)

        context['terms'] = TermsOfUse.objects.all()[0]
        return context


def suggestion(request):
    ''' View para enviar mensagens do form o que você não encontrou '''
    form_suggestion = SuggestionForm(request.POST or None)

    if  form_suggestion.is_valid():
        messages.success(request, 'Sua sugestão foi enviada com sucesso.')
        form_suggestion.save()

    return redirect(request.GET.get('url'))


def result_search(request, extra_context={}):
    """
    View para busca textual
    """
    q = request.GET.get('q', '')
    t = request.GET.getlist('t')
    activity = request.GET.getlist('activity')
    option_value = request.GET.getlist('option-value')
    locale = request.GET.getlist('locale')
    payment = request.GET.getlist('payment')
    city = request.session.get('city')

    if len(q) < 3:
        if len(q) > 0:
            messages.warning(request, u'Para buscar digite ao '
                                                u'menos 3 caracteres.')
        return redirect('appsite_home')

    qs_list_area = None
    if city:
        qs_list_area = Area.objects.filter(city=city).order_by('name')

    """
    SearchQuerySet, já retorna só os anúncios ativos.
    """
    product_list = SearchQuerySet().filter(content=q)

    qs_banner = Banner.active.all().order_by('?')

    if city:
        product_list = product_list.filter(Q
                    (city=city.city, is_national='nao') | Q(is_national='sim'))
        qs_banner = qs_banner.filter(Q(city=city) | Q(is_national=True))

    if t:
        product_list = product_list.filter(type_ad__in=t)

    if activity:
        product_list = product_list.filter(activities__in=activity)

    if option_value:
        product_list = product_list.filter(option_values__in=option_value)

    if locale:
        product_list = product_list.filter(area__id__in=locale)

    if payment:
        product_list = product_list.filter(payment__id__in=payment)

    commerce = product_list.filter(type_ad='comercio')
    service = product_list.filter(type_ad='servico')
    event = product_list.filter(type_ad='evento')
    qs_banner = qs_banner[:3]
    activities = []

    for product in product_list:
        if product.object:
            activities.extend(product.object.activities.all())
        else:
            return direct_to_template(request,
                    template='appsite/result_search.html',
                    extra_context=extra_context)

    activities = set(activities)

    extra_context.update({
        'commerce': commerce.count(),
        'service': service.count(),
        'event': event.count(),
        'q': q,
        'product_list': product_list,
        'count': product_list.count(),
        'qs_banner': qs_banner,
        'qs_list_area': qs_list_area,
        'activities': activities
    })

    return direct_to_template(request,
        template='appsite/result_search.html',
        extra_context=extra_context)

# def result_filter_category(request, extra_context={}):
#     """
#     View para busca textual
#     """
#     t = request.GET.getlist('t')
#     activity = request.GET.getlist('activity')
#     option_value = request.GET.getlist('option-value')
#     locale = request.GET.getlist('locale')
#     payment = request.GET.getlist('payment')
#     city = request.session.get('city')
#
#     qs_list_area = None
#     if city:
#         qs_list_area = Area.objects.filter(city=city).order_by('name')
#
#     """
#     SearchQuerySet, já retorna só os anúncios ativos.
#     """
#     product_list = Ad.active.all()
#
#     qs_banner = Banner.active.all().order_by('?')
#
#     if city:
#         product_list = product_list.filter(city=city.name)
#         qs_banner = qs_banner.filter(city=city)
#
#     if t:
#         product_list = product_list.filter(type_ad__in=t)
#
#     if activity:
#         product_list = product_list.filter(activities__in=activity)
#
#     if option_value:
#         product_list = product_list.filter(option_values__in=option_value)
#
#     if locale:
#         product_list = product_list.filter(area__id__in=locale)
#
#     if payment:
#         product_list = product_list.filter(payment__id__in=payment)
#
#     commerce = product_list.filter(type_ad='comercio')
#     service = product_list.filter(type_ad='servico')
#     event = product_list.filter(type_ad='evento')
#
#     activities = []
#     for product in product_list:
#         activities.extend(product.activities.all())
#
#     activities = set(activities)
#
#     extra_context.update({
#         'commerce':commerce.count(),
#         'service':service.count(),
#         'event': event.count(),
#         'ads': product_list,
#         'count': product_list.count(),
#         'qs_banner': qs_banner,
#         'qs_list_area': qs_list_area,
#         'activities': activities
#     })
#
#     return direct_to_template(request,
#         template='category/filter.html',
#         extra_context=extra_context)


class ReportFormView(FormView):
    template_name = 'appsite/report.html'
    form_class = ReportForm

    def get_initial(self):
        comment = Comment.objects.get(id=self.kwargs['comment_pk'])
        return {'comment': comment}

    def get_success_url(self):
        return reverse('report_success_view')

    def form_valid(self, form):
        form.save()  # envia e-mail
        return super(ReportFormView, self).form_valid(form)


class ReportSuccessTemplateView(TemplateView):
    template_name = 'appsite/report_success.html'
