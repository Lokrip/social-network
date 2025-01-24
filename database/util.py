from django.db import models
from django.utils.translation import gettext_lazy as _

class DateModel(models.Model):
    created_at = models.DateTimeField(_("Date created"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Date update"), auto_now=True)
    
    class Meta:
        abstract = True