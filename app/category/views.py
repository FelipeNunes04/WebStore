# coding: utf-8
from datetime import datetime, timedelta
from django.db.models import Q
from django.views.generic import DetailView
from django.template import loader, Context
from models import Activity, Category
from ads.models import Ad
from banner.models import Banner
from channel.models import Video
from locations.models import Area
from news.models import Entry
from wqti_util.json import to_json_response

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


class CategoryDetailView(DetailView):
    template_name = 'category/category_detail.html'
    context_object_name = 'category'
    model = Category

    def get_context_data(self, *args, **kwargs):
        context = super(CategoryDetailView, self).\
                    get_context_data(*args, **kwargs)

        category = context['category']
        city = self.request.session.get('city')

        qs_banner = Banner.active.filter(category=category).order_by('?')
        qs_list_videos = Video.active.filter(category=category)
        qs_news = Entry.active.filter(category=category)
        qs_list_ads = Ad.active.filter(category=category).order_by('?')
        qs_list_area = None

        if city:
            qs_list_videos = qs_list_videos.filter(
                        Q(city=city, is_national=False) | Q(is_national=True))
            qs_banner = qs_banner.filter(Q(city=city, is_national=False) |
                Q(is_national=True))
            qs_news = qs_news.filter(Q(city=city, is_national=False) |
                                                        Q(is_national=True))
            qs_list_ads = qs_list_ads.filter(Q(city=city, is_national=False) |
                Q(is_national=True))
            areas = qs_list_ads.values('area')
            qs_list_area = Area.objects.filter(pk__in=areas)

        activities = qs_list_ads.values('activities__id').distinct()
        qs_list_activity = Activity.objects.filter(pk__in=activities)\
                                                        .order_by('ordering')

        '''
        Mostrar as 8 mais clicadas de acordo com o contador(views_top),
        excluindo as que repetem na last_news,
        e com no máximo com 7 dias da data de criação.
        '''
        news_top = qs_news.exclude(
                            date_added__lt=datetime.now() - timedelta(days=2))
        news_top = news_top.order_by('-views_top')[:2]

        '''
        news_top, se não existir a lista pega outras 8 notícias mais vistas em
        todo tempo do site, e coloca em oredem aleatória
        (excluindo as do last_news)
        '''
        if news_top:
            news_top = news_top
        else:
            news_top = qs_news.order_by('-views')[:2]

        '''
        últimas notícias, aparecer somente até 7 dias de cadastro
        '''
        last_news = qs_news.\
                    exclude(date_added__lt=datetime.now() - timedelta(days=7))\
                    .exclude(pk__in=[e.pk for e in news_top]).order_by('?')[:6]

        context['news_more_views'] = news_top

        '''
        last_news, se não existir a lista pega em ordem aleatória
        outras 5 dicas.
        '''
        if last_news:
            context['last_news'] = last_news
        else:
            context['last_news'] = qs_news.all()\
                                    .exclude(pk__in=[e.pk for e in news_top])\
                                    .order_by('?')[:6]

        if qs_news.exists():
            context['qs_all_news'] = qs_news.latest('date_added')
        else:
            context['qs_all_news'] = None

        context['list_videos'] = qs_list_videos
        context['list_ads'] = qs_list_ads
        context['list_activity'] = qs_list_activity.order_by('name')

        context['qs_list_area'] = qs_list_area

        if qs_list_videos.exists():
            context['video'] = qs_list_videos.latest('date_added')
        else:
            context['video'] = None

        if qs_banner.exists():
            context['list_banner'] = qs_banner[:3]
        else:
            context['list_banner'] = None

        return context


def result_filter(request):
    """ View dos filtros laterais """
    t = request.GET.getlist('t')
    category = request.GET.get('category', '')
    activity = request.GET.get('activity', '')
    option_value = request.GET.getlist('option-value')
    locale = request.GET.getlist('locale')
    area = request.GET.getlist('area')
    payment = request.GET.getlist('payment')
    city = request.session.get('city', '')
    page_get = request.GET.get('page', '')

    ads = Ad.active
    qs_banner = Banner.active.order_by('?')
    if city:
        ads = ads.filter(Q(city=city, is_national=False) |
            Q(is_national=True))
        qs_banner = qs_banner.filter(Q(city=city, is_national=False) |
            Q(is_national=True))

    if category:
        ads = ads.filter(category__id=category)
        qs_banner = Banner.active.filter(category__pk=category)

    if activity:
        ads = ads.filter(activities__id=activity)

    for value in option_value:
        ads = ads.filter(option_values__id=value)
    if payment:
        ads = ads.filter(payment__id__in=payment)

    commerce = ads.filter(type_ad='comercio')
    service = ads.filter(type_ad='servico')
    event = ads.filter(type_ad='evento')

    if request.GET.get('t'):
        ads = ads.filter(type_ad__in=t)
    if area:
        ads = ads.filter(area__pk__in=area)
    elif locale:
        ads = ads.filter(city__id__in=locale)

    ads = ads.distinct()
    count_ads = ads.count()
    activities = ads.values('activities').distinct()

    if t == [u'']:
        t = None

    list_values = []
    for activity in activities:
        activity_id = activity['activities']
        list_ads = ads.filter(activities__id=activity_id)
        options = []
        for ad in list_ads:
            ad = ad.option_values.all().values('id')
            ad = ad.order_by('name')
            options.extend([option['id'] for option in ad])
        options = set(options)
        list_values.append((activity_id, list(options)))

    # pagination
    p = Paginator(ads, 15)

    try:
        ads = p.page(page_get).object_list
        paginator = p.page(page_get)
    except PageNotAnInteger:
        ads = p.page(1).object_list
        paginator = p.page(1)
    except EmptyPage:
        ads = p.page(p.num_pages).object_list
        paginator = p.page(p.num_pages)
    # end pagination

    if request.GET.get('page', ''):
        page_get = int(request.GET.get('page', ''))
    else:
        page_get = 1

    if not request.GET.get('activity', ''):
        activity['activities'] = ''

    template = loader.get_template('category/filter.html')
    c = Context({
        'ads': ads,
        'commerce': commerce.count(),
        'service': service.count(),
        'event': event.count(),
        'count': count_ads,
        'request': request,
        'qs_banner': qs_banner[:3],
        't': t,
        'category': category,
        'activity': activity['activities'],
        'option_value': option_value,
        'paginator': paginator,
        'list_pages': p.page_range,
        'page': page_get,  # pagina atual
    })

    rendered = template.render(c)

    return to_json_response({
        'html': rendered,
        'activities': list(list_values)})
