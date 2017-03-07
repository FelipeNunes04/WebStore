from django.db import models
from django.contrib.localflavor.br import br_states


class ZipCode(models.Model):
    zip_code = models.CharField(max_length=8, unique=True)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=2, choices=br_states.STATE_CHOICES)
    neighborhood = models.CharField(max_length=255)
    address = models.CharField(max_length=255)

    def __unicode__(self):
        return "%s" % self.zip_code
