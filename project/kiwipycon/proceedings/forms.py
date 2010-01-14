# -*- coding: utf-8 -*-

from django import forms


class ProceedingsForm(forms.Form):
    """Form for proceedings.
    """

    title = forms.CharField(required=True, label=u'Title',
                            widget=forms.TextInput(attrs={'size':'70'}))

    abstract = forms.CharField(
        widget=forms.Textarea(attrs={'cols': '80', 'rows': '8'}),
        required=True, label=u'Abstract',
        help_text=u'Upto 200 words. Content must strictly be in reSt format.')

    body = forms.CharField(
        widget=forms.Textarea(attrs={'cols': '80', 'rows': '25'}),
        required=False, label=u'Body', help_text=u'Approximately 7 pages. '
        'Content must strictly be in reSt format.')

    rst_file = forms.FileField(
        required=False, label=u'reStructuredText file',
        help_text=u'The file should contain two sections, one with a heading '
        "'Abstract' and other with a heading 'Body'.")

    self_author = forms.BooleanField(
        required=False, label=u'Author(yourself)',
        help_text=u'Check the field if you are one of the authors')

    additional_authors = forms.CharField(
        required=False, label=u'Additional Author(s)',
        help_text=u'User ID of each additional author separated by comma.')
