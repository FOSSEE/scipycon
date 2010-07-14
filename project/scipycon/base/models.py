from django.db import models


class Base(models.Model):
    """Base model which is in turn inherited by other models. 
    """
    
    scope = models.CharField(max_length=255)
