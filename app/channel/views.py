# coding: utf-8
from django.db.models import Q
from django.views.generic import DetailView, TemplateView
from models import Video
from category.models import Category


class VideoDetailView(DetailView):
    """
    Listar todos videos, e videos mais vistos,
    lista o menu esquerdo, chama a funcao para add_views do model
    """
    template_name = 'channel/channel_detail.html'
    context_object_name = 'video'
    model = Video

    def get_context_data(self, *args, **kwargs):
        context = super(VideoDetailView, self).\
                    get_context_data(*args, **kwargs)
        city = self.request.session.get('city')
        qs_videos = Video.active.filter(category=self.object.category)

        if city:
            qs_videos = qs_videos.filter(Q(city=city, is_national=False) |
                Q(is_national=True)).distinct()

        context['video_list_all'] = qs_videos.order_by('-city', '?')
        context['videos_more_viewed'] = qs_videos.order_by('-views')
        context['list_menu'] = Category.objects.all().order_by('ordering')
        video = context['video']
        video.add_views()

        return context


class VideoRefreshTemplateView(TemplateView):
    """
    Listar todos videos, e videos mais vistos,
    lista o menu esquerdo, chama a funcao para add_views do model
    """
    template_name = 'channel/channel_detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super(VideoRefreshTemplateView, self).\
                    get_context_data(*args, **kwargs)
        city = self.request.session.get('city')

        category = Category.objects.get(slug=self.kwargs['slug'])

        qs_video_list_all = Video.active\
            .filter(category=category).order_by('?')
        qs_videos_more_viewed = Video.active\
            .filter(category=category).order_by('-views')
        if city:
            qs_video_list_all = qs_video_list_all.filter(
                                        Q(city=city, is_national=False) |
                                            Q(is_national=True)).distinct()
            qs_videos_more_viewed = qs_videos_more_viewed.filter(
                                        Q(city=city, is_national=False) |
                                            Q(is_national=True)).distinct()

        context['video_list_all'] = qs_video_list_all
        context['videos_more_viewed'] = qs_videos_more_viewed
        context['list_menu'] = Category.objects.all().order_by('ordering')
        if Video.active.filter(category=category).exists():
            context['video'] = Video.active.filter(category=category)\
                                                    .order_by('date_added')[0]
            context['video'].add_views()

        if context:
            return context
        else:
            return {'context': False}
