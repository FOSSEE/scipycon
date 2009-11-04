# -*- coding: utf-8 -*-
from __future__ import absolute_import

#django
from django.db import models
from django.contrib.auth.models import User

#tagging
from tagging import register
from tagging.fields import TagField
from tagging.utils import parse_tag_input

DURATION_CHOICES = (
    ('10', 'Lightning Talk (10 mins)'),
    ('20', 'Short Talk (20 mins)'),
    ('30', 'Standard Talk (30 mins)'),
    )

AUDIENCE_CHOICES = (
    ('nonprogrammers', 'non-programmer'),
    ('beginers', 'beginning programmer'),
    ('intermediate', 'intermediate programmer'),
    ('advanced', 'advanced programmer'),
    )

#TOPIC_CHOICES = (
#    ('Core Python', 'Core Python'),
#    ('Other implementations: Jython, IronPython, PyPy, and Stackless', 'Other implementations: Jython, IronPython, PyPy, and Stackless'),
#    ('Python libraries and extensions', 'Python libraries and extensions'),
#    ('Python 3k', 'Python 3k'),
#    ('Databases', 'Databases'),
#    ('Documentation', 'Documentation'),
#    ('GUI Programming', 'GUI Programming'),
#    ('Game Programming', 'Game Programming'),
#    ('Network Programming', 'Network Programming'),
#    ('Open Source Python projects', 'Open Source Python projects'),
#    ('Packaging Issues', 'Packaging Issues'),
#    ('Programming Tools', 'Programming Tools'),
#    ('Project Best Practices', 'Project Best Practices'),
#    ('Embedding and Extending', 'Embedding and Extending'),
#    ('Science and Maths', 'Science and Maths'),
#    ('Web-based Systems', 'Web-based Systems'),
#)

class Talk(models.Model):
    """Defines talks at *PyCon"""
    slug = models.SlugField()
    speaker = models.ForeignKey(User)
    authors_bio = models.TextField()
    contact = models.EmailField()
    title = models.CharField(max_length=1024)
    abstract = models.TextField()
#    outline = models.TextField()
    topic = models.CharField(max_length=255, 
                             #choices=TOPIC_CHOICES,
                             blank=True)
#    topic_other = models.CharField(max_length=255, blank=True)
    duration = models.CharField(max_length=3, choices=DURATION_CHOICES)
    audience = models.CharField(max_length=32, choices=AUDIENCE_CHOICES, blank=True)
#    audience_other = models.CharField(max_length=128, blank=True)
    approved = models.BooleanField(default=False)
    submitted = models.DateTimeField(auto_now_add=True)
    last_mod = models.DateTimeField(auto_now=True)
#    tags = TagField(blank=True)

    def __unicode__(self):
        return self.title

    def get_tag_list(self):
        return parse_tag_input(self.tags)

# register(Talk) # saving talk failed - see:
# http://code.google.com/p/django-tagging/issues/detail?id=152
