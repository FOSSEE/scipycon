from django.db import models
from django.contrib.auth.models import User

from tagging import register
from tagging.fields import TagField
from tagging.utils import parse_tag_input

from project.scipycon.base import models as base_models


DURATION_CHOICES = (
    ('10', 'Lightning Talk (10 mins)'),
    ('20', 'Short Talk (20 mins)'),
    ('30', 'Standard Talk (30 mins)'),
    )

AUDIENCE_CHOICES = (
    ('nonprogrammers', 'Non Programmer'),
    ('beginers', 'Beginner Programmer'),
    ('intermediate', 'Intermediate Programmer'),
    ('advanced', 'Advanced Programmer'),
    )


class Talk(base_models.ScopedBase):
    """Defines talks at SciPy.in
    """

    slug = models.SlugField()

    speaker = models.ForeignKey(User)

    authors_bio = models.TextField()

    contact = models.EmailField()

    title = models.CharField(max_length=1024)

    abstract = models.TextField()

    topic = models.CharField(max_length=255, blank=True)

    duration = models.CharField(max_length=3, choices=DURATION_CHOICES)

    audience = models.CharField(max_length=32, choices=AUDIENCE_CHOICES, blank=True)

    approved = models.BooleanField(default=False)

    submitted = models.DateTimeField(auto_now_add=True)

    last_mod = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.title

    def get_tag_list(self):
        return parse_tag_input(self.tags)
