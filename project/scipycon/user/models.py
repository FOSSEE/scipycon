from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.contrib.auth.models import User

from project.scipycon.base import models as base_models


class UserProfile(base_models.Base):
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

def add_profile(sender, instance, signal, *args, **kwargs):
    """Create user profile on create of new user"""
    if not instance.is_superuser:
        try:
            profile, new = UserProfile.objects.get_or_create(user=instance)
            if new:
                profile.save()
        except:
            pass

post_save.connect(add_profile, sender=User, weak=False)
