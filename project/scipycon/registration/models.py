# -*- coding: utf-8 -*-
from __future__ import absolute_import

#django
from django.db import models
from django.contrib.auth.models import User

from .utils import send_confirmation_payment_email
from .utils import send_banking_fix_email

from .labels import WIFI_CHOICES
from .labels import WIFI_HELP

SIZE_CHOICES = (
    ('S', 'S'),
    ('M', 'M'),
    ('L', 'L'),
    ('XL', 'XL'),
    )

class Wifi(models.Model):
    """Defines wifi options at *PyCon"""
    user = models.ForeignKey(User)
    wifi = models.CharField(max_length=50, choices=WIFI_CHOICES,
            help_text=WIFI_HELP, verbose_name="Laptop")

class Registration(models.Model):
    """Defines registration at *PyCon"""
    slug = models.SlugField()
    registrant = models.ForeignKey(User)
    organisation = models.CharField(max_length=255, blank=True)
    occupation = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255, blank=True)
    postcode = models.CharField(max_length=255, blank=True)
#    beverage = models.CharField(max_length=255, blank=True)
#    diet = models.CharField(max_length=255, blank=True)
#    sponsor = models.CharField(max_length=255, blank=True)
    tshirt = models.CharField(max_length=2, choices=SIZE_CHOICES)
#    party = models.BooleanField(default=False)
#    discount = models.BooleanField(default=False)

    # scipy.in specific
    conference = models.BooleanField(default=False)
    # scipy.in specific
    tutorial = models.BooleanField(default=False)
    # scipy.in specific
    sprint = models.BooleanField(default=False)

#    amount = models.IntegerField(default=0)
    allow_contact = models.BooleanField(default=False)
#    payment = models.BooleanField(default=False)
    submitted = models.DateTimeField(auto_now_add=True)
    last_mod = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return 'Registration for user: <%s %s> %s' % (self.registrant.first_name,
                self.registrant.last_name, self.registrant.email)

#    def save(self, *args, **kwargs):
#        if(self.id):
#            old_reg = Registration.objects.get(pk=self.id)
#            if(old_reg.payment == False and self.payment == True \
#                    and not self.sponsor):
#                send_confirmation_payment_email(self.registrant)
#            if(old_reg.slug.startswith('NZ') and self.slug.startswith('KPC') \
#                    and not self.sponsor):
#                send_banking_fix_email(self.registrant, self.slug)
#        super(Registration, self).save(args, kwargs)
