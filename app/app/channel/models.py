# coding: utf-8
from datetime import datetime
from django.db import models
from django.utils import simplejson
import urllib
import os
import requests
from django.conf import settings
from category.models import Category
from locations.models import City
from manager import ActiveVideoManager


class Video(models.Model):
    category = models.ForeignKey(Category)
    title = models.CharField(u'título', max_length='128', )
    description = models.TextField(u'descrição', )
    video = models.CharField(u'url do video', max_length=256,
                help_text=' url= http://www.youtube.com/watch?v=rWlHtvZHbZ', )
    city = models.ForeignKey(City)
    views = models.IntegerField(u'views em cada vídeo', default=0, )
    slug = models.SlugField(u'slug', unique=True, max_length=32, )
    image = models.CharField(max_length=256, editable=False, null=True,
                blank=True, )
    date_added = models.DateTimeField(u'data de criação do video',
                                        default=datetime.now(), )
    date_expires = models.DateTimeField(u'data de expiração do vídeo',
        null=True, blank=True,
        help_text=u'deixe em branco caso o vídeo não expire')
    is_national = models.BooleanField(u'publicação nacional', default=False)
    active = ActiveVideoManager()
    objects = models.Manager()

    class Meta:
        verbose_name, verbose_name_plural = u'Vídeo', u'Vídeos'

    def __unicode__(self):
        return self.title

    """
    Soma uma view ao video
    """

    def add_views(self):
        self.views += 1
        self.save()

    """
    Utiliza url do video add pelo admin e pega a imagem dela
    para thub no servidor do youtube
    """

    def get_image(self):
        if self.video.count('youtube'):
            return "http://img.youtube.com/vi/%s/0.jpg" % \
                                                self.video.split('?v=')[-1]
        else:
            request = requests.get(("http://vimeo.com/api/v2/video/%s.json") \
                                                % self.video.split('/')[-1])
            data = simplejson.loads(request.content)[0]
            return data.get('thumbnail_small', '')

    def save(self, *args, **kwargs):
        file = urllib.urlopen(self.get_image())
        upload_full_path = '%s/thumbs/%s.jpg' % (settings.MEDIA_ROOT,
                            self.slug)
        dest = open(os.path.join(upload_full_path), 'wb+')
        dest.write(file.read())
        dest.close
        self.image = 'thumbs/%s.jpg' % self.slug

        return super(Video, self).save(*args, **kwargs)


# class VideoModerator(CommentModerator):
#     email_notification = False
#
# moderator.register(Video, VideoModerator)
#
# signals.pre_save.connect(moderate_comment, sender=Comment)
