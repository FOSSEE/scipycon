# -*- coding: utf-8 -*-
from __future__ import absolute_import

#django
from django import forms
from django.core.exceptions import ObjectDoesNotExist

#django.contrib
from django.contrib.auth.models import User

from .models import SIZE_CHOICES
from .models import Registration
from .models import Wifi


class RegistrationSubmitForm(forms.Form):
    """PyCon registration form
    """
    tshirt = forms.ChoiceField(choices=SIZE_CHOICES, required=True,
        label=u'T-shirt size', help_text=u'Yes, we all get a t-shirt!')
    organisation = forms.CharField(required=True, label=u'Organisation',
        help_text=u'The primary organisation that you are a member of.',
        max_length=255,
        widget=forms.TextInput(attrs={'size':'50'}))
    occupation = forms.CharField(required=True, label=u'Occupation',
        help_text=u'Title of your occupation',
        max_length=255,
        widget=forms.TextInput(attrs={'size':'50'}))
    city = forms.CharField(required=True, label=u'City',
        help_text=u'City of residence',
        max_length=255,
        widget=forms.TextInput(attrs={'size':'50'}))
    postcode = forms.CharField(required=False, label=u'Postcode',
        help_text=u'This field is optional',
        max_length=10,
        widget=forms.TextInput(attrs={'size':'10'}))
    allow_contact = forms.BooleanField(required=False, label=u'Contact',
        help_text=u'May organizers of SciPy.in contact you after the event?')
    conference = forms.BooleanField(required=False, label=u'Conference',
        help_text=u"""Do you intend to attend the SciPy conference?  
        Note: Only conference has an registration fee of Rs.200 which you will
        pay on the spot.""")
    tutorial = forms.BooleanField(required=False, label=u'Tutorial',
        help_text=u'Do you intend to attend the tutorials?')
    sprint = forms.BooleanField(required=False, label=u'Sprint',
        help_text=u'Do you intend to attend the sprints?')

    def demographic_fields(self):
        return (self['organisation'],
                self['occupation'],
                self['city'],
                self['postcode'])

    def personal_fields(self):
        return (self['tshirt'],
                self['conference'],
                self['tutorial'],
                self['sprint'],
                self['allow_contact'])


class RegistrationEditForm(RegistrationSubmitForm):
    id = forms.CharField(widget=forms.HiddenInput)
    sponsor = forms.CharField(required=False, widget=forms.HiddenInput)

class WifiForm(forms.ModelForm):
    """PyCon wifi form
    """

    def save(self, user):
        wifi = Wifi(user=user, wifi=self.cleaned_data['wifi'])
        wifi.save()
        return wifi

    class Meta:
        model = Wifi
        fields = ('wifi',)

PC = (
        ('all', 'all'),
        ('paid', 'paid'),
        ('not paid', 'not paid')
        )
HC = (
        ('all', 'all'),
        ('party', 'party'),
        ('no party', 'no party')
        )
AC = (
        ('all', 'all'),
        ('0', '0'),
        ('10', '10'),
        ('20', '20'),
        ('40', '40'),
        )
OC = (
        ('email', 'email'),
        ('amount', 'amount'),
        )

IC = (
        ('Name', 'name'),
        ('Email', 'email'),
        ('Amount', 'amount'),
        ('Organisation', 'organisation'),
        ('Conference', 'conference'),
        ('Tutorial', 'tutorial'),
        ('Sprint', 'sprint'),
        ('T-size', 'tshirt'),
        )

SC = (
    ('all', 'all'),
    ('S', 'S'),
    ('M', 'M'),
    ('L', 'L'),
    ('XL', 'XL'),
    )
class RegistrationAdminSelectForm(forms.Form):
    """
    Used to make selection for csv download
    """
    by_payment = forms.ChoiceField(choices=PC, required=False,
        label=u'By payment')
    by_amount = forms.MultipleChoiceField(choices=AC, required=False,
        label=u'By amount')
    by_party = forms.ChoiceField(choices=HC, required=False,
        label=u'by party')
    by_tshirt = forms.ChoiceField(choices=SC, required=False,
        label=u'by tshirt size')
    order_by = forms.ChoiceField(choices=OC, required=False,
        label=u'order results')
    include = forms.MultipleChoiceField(choices=IC, required=False,
        label=u'Include fields')
