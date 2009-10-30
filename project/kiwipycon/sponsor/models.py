# -*- coding: utf-8 -*-
from __future__ import absolute_import

#django
from django.db import models
from django.conf import settings

TYPE_CHOICES = (
    ('gold', 'Gold'),
    ('silver', 'Silver'),
    ('schwag', 'Schwag'),
    )

class Sponsor(models.Model):
    """Defines sponsors for *PyCon"""
    slug = models.SlugField()
    title = models.CharField(max_length=255)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    contact_name = models.CharField(max_length=255)
    contact_email = models.CharField(max_length=255)
    contact_phone = models.CharField(max_length=255)
    url = models.URLField(blank=True, verify_exists=False)
    logo = models.CharField(max_length=64, blank=True)
    guests = models.IntegerField()

    def __unicode__(self):
        return self.title

