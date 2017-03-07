#coding: utf-8
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save
from wqti_util.email import EmailMessage


def moderate_comment(sender, instance, **kwargs):
    ''' O teste instance.content_type deve ser alterado para 18 sempre que 
        que for ao subir, o content_type.id de anúncios é 18. 
        E local Aguirres 20.
    ''' 
    if instance.content_type.id == 18:
        if not instance.id:
            instance.is_public = False
        else:
            pass
    else: 
        pass


def authorized_comment(sender, comment, request, **kwargs):
    from models import Ad
    try: 
        ad = Ad.objects.get(pk=comment.object_pk)
        message = EmailMessage(
            to= ad.user.email,
            subject='Contato do site Virtuallia',
            template='comments/comment_authorization.txt',
            context={'comment': comment, }
        )
        message.send()
    except:
        pass