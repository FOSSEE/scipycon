from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.contrib.auth.models import User

from project.scipycon.base import models as base_models


class UserProfile(base_models.ScopedBase):
    """Extend atributes for django User
    """

    user = models.ForeignKey(User, unique=True)

    url = models.URLField(blank=True, verify_exists=False)

    photo = models.CharField(max_length=64, blank=True)

    about = models.TextField(blank=True)

    def __unicode__(self):
        return 'UserProfile for user: <%s %s> %s' % (self.user.first_name,
                self.user.last_name, self.user.email)

    def fullname(self):
        return '%s %s' % (self.user.first_name, self.user.last_name)
