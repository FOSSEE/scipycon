# -*- coding: utf-8 -*-
from __future__ import absolute_import

#django
from django import forms
from django.contrib.auth.models import User

class RegistrantForm(forms.Form):
    """Form to register an attendee
    """
    username = forms.RegexField(label="Nickname", max_length=30,
            regex=r'^\w+$',
        help_text = "30 characters or fewer. Alphanumeric" \
            + " characters only (letters, digits and underscores).",
        error_message = "This value must contain only letters, numbers and underscores.")
    name = forms.CharField(label=u"Name", max_length=50, required=True)
    email = forms.EmailField(label=u"E-mail", max_length=50, required=True)

    def clean_email(self):
        """Validates that the entered e-mail is unique.
        """
        email = self.cleaned_data.get("email")
        if email and User.objects.filter(email=email).count() > 0:
            raise forms.ValidationError(
                u"That email address is already in use. Are you a member of " \
                 "site? Please log in.")

        return email

    def clean_username(self):
        """Validates that the entered username is unique.
        """
        username = self.cleaned_data.get("username")
        if username and User.objects.filter(username=username).count() > 0:
            raise forms.ValidationError(
                u"That username is already in use.")

        return username

class RegisterForm(forms.Form):
    """Form to register speaker
    """
    username = forms.RegexField(label="Username", max_length=30,
            regex=r'^\w+$',
        help_text = "Required. 30 characters or fewer. Alphanumeric" \
            + " characters only (letters, digits and underscores).",
        error_message = "This value must contain only letters, numbers and underscores.")
    first_name = forms.CharField(label=u"First name", max_length=50)
    last_name = forms.CharField(label=u"Last name", max_length=50)
    email = forms.EmailField(label=u"E-mail", max_length=50)
    url = forms.URLField(required=False)
    about = forms.CharField(label=u'Short Bio', max_length=50, required=False)
    photo = forms.FileField(label=u'Profile Photo', required=False)
    password_1 = forms.CharField(
        label=u"Password", widget=forms.PasswordInput(), max_length=20)
    password_2 = forms.CharField(
        label=u"Confirm password", widget=forms.PasswordInput(), max_length=20)

    def clean_password_2(self):
        """Validates that password 1 and password 2 are the same.
        """
        p1 = self.cleaned_data.get('password_1')
        p2 = self.cleaned_data.get('password_2')

        if not (p1 and p2 and p1 == p2):
            raise forms.ValidationError(u"The two passwords do not match.")

        return p2

    def clean_email(self):
        """Validates that the entered e-mail is unique.
        """
        email = self.cleaned_data.get("email")
        if email and User.objects.filter(email=email).count() > 0:
            raise forms.ValidationError(
                u"That email address is already in use.")

        return email

    def clean_username(self):
        """Validates that the entered username is unique.
        """
        username = self.cleaned_data.get("username")
        if username and User.objects.filter(username=username).count() > 0:
            raise forms.ValidationError(
                u"That username is already in use.")

        return username

class EditProfileForm(forms.Form):
    """Edit user profile form
    """
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    email = forms.EmailField(max_length=50)
    email2 = forms.CharField(widget=forms.HiddenInput)
    url = forms.URLField(required=False)
    about = forms.CharField(label=u'Short Bio',
            widget=forms.Textarea, required=False)
    photo = forms.FileField(label=u'Profile Photo',
            required=False)

    def clean_email(self):
        """Validates that the entered e-mail is unique.
        """
        email = self.cleaned_data.get("email")
        email2 = self.data.get("email2").strip()
        print email, email2
        if email != email2: # email has been changed
            if email and User.objects.filter(email=email).count() > 0:
                raise forms.ValidationError(
                    u"That email address is already in use.")

        return email

class UsernameForm(forms.Form):
    """Form to edit email address
    """
    username = forms.RegexField(label="Username", max_length=30,
            regex=r'^\w+$',
        help_text = "Required. 30 characters or fewer. Alphanumeric" \
            + " characters only (letters, digits and underscores).",
        error_message = "This value must contain only letters, numbers and underscores.")

    def clean_username(self):
        """Validates that the entered username is unique.
        """
        username = self.cleaned_data.get("username")
        if username and User.objects.filter(username=username).count() > 0:
            raise forms.ValidationError(
                u"That username is already in use.")

        return username


