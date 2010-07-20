from django.db import models
from django.contrib.auth.models import User

from project.scipycon.base import models as base_models

from project.scipycon.registration.labels import WIFI_CHOICES
from project.scipycon.registration.labels import WIFI_HELP
from project.scipycon.registration.utils import send_confirmation_payment_email
from project.scipycon.registration.utils import send_banking_fix_email


SIZE_CHOICES = (
    ('S', 'S'),
    ('M', 'M'),
    ('L', 'L'),
    ('XL', 'XL'),
    )


class Wifi(base_models.ScopedBase):
    """Defines wifi options at SciPy.in
    """
    user = models.ForeignKey(User)

    wifi = models.CharField(max_length=50, choices=WIFI_CHOICES,
                            help_text=WIFI_HELP, verbose_name="Laptop")


class Registration(base_models.ScopedBase):
    """Defines registration at SciPy.in"""

    slug = models.SlugField()

    registrant = models.ForeignKey(User)

    organisation = models.CharField(max_length=255, blank=True)

    occupation = models.CharField(max_length=255, blank=True)

    city = models.CharField(max_length=255, blank=True)

    postcode = models.CharField(max_length=255, blank=True)

    phone_num = models.CharField(max_length=14, blank=True)

    tshirt = models.CharField(max_length=2, choices=SIZE_CHOICES)

    conference = models.BooleanField(default=False)

    tutorial = models.BooleanField(default=False)

    sprint = models.BooleanField(default=False)

    final_conference = models.BooleanField(default=False)

    final_tutorial = models.BooleanField(default=False)

    final_sprint = models.BooleanField(default=False)

    allow_contact = models.BooleanField(default=False)

    submitted = models.DateTimeField(auto_now_add=True)

    last_mod = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return 'Registration for user: <%s %s> %s' % (
            self.registrant.first_name,
            self.registrant.last_name, self.registrant.email)
