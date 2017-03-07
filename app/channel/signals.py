def moderate_comment(sender, instance, **kwargs):
    if not instance.id:
        instance.is_public = True