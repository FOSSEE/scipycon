from django.db import models
from django.contrib.auth.models import User

from project.scipycon.base import models as base_models

from project.scipycon.registration.labels import WIFI_CHOICES
from project.scipycon.registration.labels import WIFI_HELP


SIZE_CHOICES = (
    ('S', 'S'),
    ('M', 'M'),
    ('L', 'L'),
    ('XL', 'XL'),
    ('XXL', 'XXL'),
    )

OCCUPATION_CHOICES = (
    ('Education: Student', 'Education: Student'),
    ('Education: Faculty', 'Education: Faculty'),
    ('Education: Research', 'Education: Research'),
    ('Education: Other', 'Education: Other'),
    ('Corporate: Research', 'Corporate: Research'),
    ('Corporate: Other', 'Corporate: Other'),
    ('Other', 'Other')
    )

SEX_CHOICES = (
    ('Male', 'Male'),
    ('Female', 'Female'),
    )

PAYMENT_MODE_CHOICES = (
    ('Cheque', 'Cheque'),
    ('Demand Draft(DD)', 'Demand Draft(DD)'),
    ('Net Banking', 'Net Banking')
    )


class Wifi(base_models.ScopedBase):
    """Defines wifi options at SciPy.in
    """

    user = models.ForeignKey(User)

    wifi = models.CharField(max_length=50, choices=WIFI_CHOICES,
                            help_text=WIFI_HELP, verbose_name="Laptop")

    registration_id = models.CharField(
        max_length=255, verbose_name="Identification Number",
        help_text="- Provide the serial or identification number at the "
        "back of your laptop using which your laptop can be uniquely "
        "identified. Ex: 8BDB8FB (Service Tag on Dell Laptops).<br /> - "
        "This is for security reasons and will be used while you enter and "
        "leave the venue.<br /> - Please don't provide the model number "
        "like Dell Inspiron 1545. There may be many laptops of that model "
        "and hence your laptop cannot be uniquely identified.",
        blank=True, null=True)


class Accommodation(base_models.ScopedBase):
    """Defines accommodation information for SciPy.in
    """

    user = models.ForeignKey(User)

    sex = models.CharField(max_length=50, choices=SEX_CHOICES,
                           verbose_name="Gender",
                           blank=True, null=True)

    accommodation_required = models.BooleanField(
        default=False, blank=True,
        verbose_name="Accommodation required",
        help_text="Check if you need accommodation.")

    accommodation_days = models.IntegerField(
        default=0, blank=True,
        verbose_name="Number of days",
        help_text="Number of days the accommodation is required for?")


class Registration(base_models.ScopedBase):
    """Defines registration at SciPy.in"""

    slug = models.SlugField()

    registrant = models.ForeignKey(User)

    organisation = models.CharField(max_length=255, blank=True)

    occupation = models.CharField(max_length=255,
                                  choices=OCCUPATION_CHOICES, blank=True)

    city = models.CharField(max_length=255, blank=True)

    postcode = models.CharField(max_length=255, blank=True)

    phone_num = models.CharField(max_length=14, blank=True)

    tshirt = models.CharField(max_length=3, choices=SIZE_CHOICES)

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


class Payment(base_models.ScopedBase):
    """Defines payment information for SciPy.in registrants
    """

    user = models.ForeignKey(User)

    confirmed = models.BooleanField(
        default=False, blank=True)

    acco_confirmed = models.BooleanField(
        default=False, blank=True)

    date_confirmed = models.DateTimeField(blank=True, null=True)

    confirmed_mail = models.BooleanField(
        default=False, blank=True)

    acco_confirmed_mail = models.BooleanField(
        default=False, blank=True)

    type = models.CharField(max_length=25, choices=PAYMENT_MODE_CHOICES,
                            verbose_name="Type", blank=True, null=True)

    details = models.CharField(
        max_length=255, verbose_name="Details",
        help_text="If the payment mode was cheque or DD please provide "
        "the <font color='red'>cheque or DD number and the name of the bank "
        "and branch</font>. Example: 4536234, SBI, IIT Powai, Mumbai.<br/> "
        "If the payment mode was Net Banking please provide the <font "
        "color='red'>last four digits of the account number and the name "
        "of the account holder and the bank name</font> from which the "
        "transfer was made. Example: 8804, Harish Chandra, SBI",
        blank=True, null=True)
