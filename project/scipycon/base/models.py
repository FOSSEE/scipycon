from django.db import models


class ScopedBase(models.Model):
    """Base model which is in turn inherited by other models. 
    """

    scope = models.CharField(max_length=255)

    class Meta:
        abstract = True
