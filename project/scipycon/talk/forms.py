# -*- coding: utf-8 -*-
from __future__ import absolute_import

#django
from django import forms

#django.contrib
from django.contrib.auth.models import User

#tagging
from tagging.forms import TagField

#scipycon
#from .models import TOPIC_CHOICES
from .models import DURATION_CHOICES
from .models import AUDIENCE_CHOICES


class TalkSubmitForm(forms.Form):
    """Submit talk form
    """
    authors_bio = forms.CharField(widget=forms.Textarea, required=True,
        label=u'Author(s) and short bio',
        help_text=u'(include a bit about your qualifications regarding your presentation topic)')
    contact = forms.EmailField(required=True, label=u'E-Mail ID',
        help_text=u'Provide your email ID',
        max_length=1024,
        widget=forms.TextInput(attrs={'size':'50'}))
    title = forms.CharField(required=True, label=u'Talk title',
        help_text=u'Title of proposed presentation',
        max_length=1024,
        widget=forms.TextInput(attrs={'size':'50'}))
    abstract = forms.CharField(widget=forms.Textarea, required=True,
        help_text=u'Summary of proposed presentation (In 300-700 words)')
#    outline = forms.CharField(widget=forms.Textarea, required=True,
#        help_text=u'Outline of proposed presentation (around 200 words)')
#    topic = forms.ChoiceField(choices=TOPIC_CHOICES,
#        label=u'Topic', help_text=u'Select one of the available options or enter other topic')
#    topic_other = forms.CharField(label=u'Other topic',
#        help_text=u'Description of your topic',
#        max_length=255,
#        required=False,
#        widget=forms.TextInput(attrs={'size':'50'}))
    topic = forms.CharField(label=u'Topic',
        help_text=u'Description of your topic or comma separated tags',
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={'size':'50'}))
    duration = forms.ChoiceField(choices=DURATION_CHOICES, required=True,
        label=u'Preferred time slot', help_text=u'Select preferred time slot')
    audience = forms.ChoiceField(choices=AUDIENCE_CHOICES, label=u'Intended audience',
        help_text=u'Select one of the available options or enter other type of intended audience')
#    audience_other = forms.CharField(label=u'Other intended audience',
#        help_text=u'Description of intended audience (ie. Discordians)',
#        max_length=128,
#        required=False,
#        widget=forms.TextInput(attrs={'size':'50'}))
#    tags = TagField(max_length=255,
#        widget=forms.TextInput(attrs={'size':'50'}))

class TalkEditForm(TalkSubmitForm):
    id = forms.CharField(widget=forms.HiddenInput)
