# coding: utf-8
from django.template import Library, Node
from django.db.models import get_model
from ads.models import Ad, Signature
from channel.models import Video
from news.models import Entry

register = Library()


class ListAds(Node):

    def render(self, context):
        ads = Ad.objects.all().order_by('-views')[:10]
        context['ads'] = ads
        return ''


def get_list_ads(parser, token):
    return ListAds()

get_list_ads = register.tag(get_list_ads)


class ListNews(Node):

    def render(self, context):
        news = Entry.objects.all().order_by('-views')[:10]
        context['news'] = news
        return ''


def get_list_news(parser, token):
    return ListNews()

get_list_news = register.tag(get_list_news)


class ListVideos(Node):

    def render(self, context):
        videos = Video.objects.all().order_by('-views')[:10]
        context['videos'] = videos
        return ''

def get_list_videos(parser, token):
    return ListVideos()

get_list_videos = register.tag(get_list_videos)


class ListSignatures(Node):

    def render(self, context):
        signatures = Signature.objects.filter(is_active=True).order_by('end_date')[:10]
        signatures_inactive = Signature.objects.filter(is_active=False).order_by('start_date')[:10]
        context['signatures'] = signatures
        context['signatures_inactive'] = signatures_inactive
        return ''


def get_list_signatures(parser, token):
    return ListSignatures()

get_list_signatures = register.tag(get_list_signatures)
