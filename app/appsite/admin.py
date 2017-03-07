#coding: utf-8
from django.contrib import admin
from django.contrib.comments.models import Comment
from django.contrib.comments.admin import CommentsAdmin
from models import Corporate, PrivacyPolicy, TermsOfUse
from django.contrib.admin.views.decorators import staff_member_required
import os
from uuid import uuid4
from django.conf import settings
from django.http import HttpResponse


class MyCommentsAdmin(CommentsAdmin):
    list_filter = ('submit_date', 'site', 'is_public', 'is_removed',
                                                            'content_type')


admin.site.unregister(Comment)
admin.site.register(Comment, MyCommentsAdmin)
admin.site.register(Corporate, )
admin.site.register(PrivacyPolicy, )
admin.site.register(TermsOfUse, )


@staff_member_required
def image_upload(request):
    """
    Fazer upload de imagem
    """
    try:
        upload_full_path = '%s/content/images/' % settings.MEDIA_ROOT
        upload = request.FILES['image']
        filename = '%s.%s' % (uuid4(), upload.name.split('.')[-1])
        dest = open(os.path.join(upload_full_path, filename), 'wb+')

        for chunk in upload.chunks():
            dest.write(chunk)
        dest.close()

        result = '{status:"UPLOADED", image_url:"%s"}' %\
            ('%s/content/images/%s' % (settings.MEDIA_URL, filename))

        return HttpResponse(result, mimetype='text/html')

    except Exception:
        return HttpResponse("error")
