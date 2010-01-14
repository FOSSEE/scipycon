# -*- coding: utf-8 -*-
from __future__ import absolute_import

from django.db import models
from django.contrib.auth.models import User


class Paper(models.Model):
    """Data model for storing proceedings paper.
    """

    title = models.CharField(max_length=200)
    abstract = models.TextField()
    body = models.TextField()
