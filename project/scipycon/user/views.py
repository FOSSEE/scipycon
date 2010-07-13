# -*- coding: utf-8 -*-
from __future__ import absolute_import

#python
from urlparse import urlparse
import simplejson as json
import urllib
import os

#django
from django.conf import settings
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.db.models.signals import post_save

#django.contrib
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

#PIL
from PIL import Image

#scipycon
from project.scipycon.utils import set_message_cookie
from project.scipycon.talk.models import Talk
from project.scipycon.registration.models import Registration
from project.scipycon.registration.models import Wifi
from project.scipycon.registration.forms import WifiForm

from .utils import scipycon_createuser
from .utils import handle_uploaded_photo
from .forms import RegisterForm
from .forms import EditProfileForm
from .forms import UsernameForm

@login_required
def account(request, template_name="user/account.html"):
    """Displays the main screen of the current user's account.
    """
    user = request.user
    profile = user.get_profile()

    talks = Talk.objects.filter(speaker=user)
    try:
        registration = Registration.objects.get(registrant=user)
    except ObjectDoesNotExist:
        registration = None
    try:
        wifiobj = Wifi.objects.get(user=user)
    except ObjectDoesNotExist:
        wifiobj = None

    if profile.photo:
        photo = os.path.join(settings.USER_MEDIA_URL, profile.photo)
    else:
        photo = '/img/user-default.png'

    qstring = ""

    wifi_comment = None
    if wifiobj:
        wifi_form = False
    else:
        if request.method == "POST":
            wifi_form = WifiForm(request.POST)
            if wifi_form.is_valid():
                wifi_form.save(user)
            wifi_comment = 'Thanks, your wifi preference has been saved'
            wifi_form = None
        else:
            wifi_form = WifiForm()

    return render_to_response(template_name, RequestContext(request, {
        "form" : wifi_form, "comment": wifi_comment,
        "user" : user, "profile" : profile, "photo" : photo,
        "talks" : talks, "registration" : registration,
    }))

@login_required
def edit_profile(request, template_name="user/editprofile.html"):
    """Allows user to edit profile
    """
    user = request.user
    profile = user.get_profile()

    if request.method == "POST":
        form = EditProfileForm(data=request.POST,
                               files=request.FILES)

        if form.is_valid():
            photo = request.FILES.get('photo', None)
            filename= None
            if photo:
                filename = handle_uploaded_photo(user, request.FILES['photo'])
            if filename:
                profile.photo = filename

            user.email = form.data.get("email")
            user.first_name = form.data.get("first_name")
            user.last_name = form.data.get("last_name")
            user.save()

            profile.url = form.data.get("url")
            profile.about = form.data.get("about")
            profile.save()

            redirect_to = reverse("scipycon_account")
            return set_message_cookie(redirect_to,
                    msg = u"Your profile has been changed.")

    else:
        form = EditProfileForm(initial={"email" : user.email,
                                        "email2" : user.email, # hidden field
                                        "first_name" : user.first_name,
                                        "last_name" : user.last_name,
                                        "url" : profile.url,
                                        "about" : profile.about,
                                        })

    return render_to_response(template_name, RequestContext(request, {
        "form": form
    }))

def login(request, template_name="user/login.html"):
    """Custom view to login or register/login a user.
    Integration of register and login form
    It uses Django's standard AuthenticationForm, though.
    """
    user = request.user
    if user.is_authenticated():
        redirect_to = reverse("scipycon_account")
        return set_message_cookie(redirect_to,
                msg = u"Redirected to account from login form.")

    # Using Djangos default AuthenticationForm
    login_form = AuthenticationForm()
    register_form = RegisterForm()

    if request.POST.get("action") == "login":
        login_form = AuthenticationForm(data=request.POST)

        if login_form.is_valid():
            redirect_to = request.POST.get("next")
            # Light security check -- make sure redirect_to isn't garbage.
            if not redirect_to or '//' in redirect_to or ' ' in redirect_to:
                redirect_to = reverse("scipycon_account")

            from django.contrib.auth import login
            login(request, login_form.get_user())

            return set_message_cookie(redirect_to, msg = u"You have been logged in.")

    elif request.POST.get("action") == "register":
        register_form = RegisterForm(data=request.POST)
        if register_form.is_valid():

            user = scipycon_createuser(request, register_form.data)

            redirect_to = request.POST.get("next")
            if not redirect_to or '//' in redirect_to or ' ' in redirect_to:
                redirect_to = reverse("scipycon_account")

            return set_message_cookie(
                redirect_to, msg = u"You have been registered and logged in.")

    # Get next_url
    next_url = request.REQUEST.get("next")
    if next_url is None:
        next_url = request.META.get("HTTP_REFERER")
    if next_url is None:
        next_url = reverse("scipycon_account")
    # Get just the path of the url. See django.contrib.auth.views.login for more
    next_url = urlparse(next_url)
    next_url = next_url[2]

    try:
        login_form_errors = login_form.errors["__all__"]
    except KeyError:
        login_form_errors = None

    return render_to_response(template_name, RequestContext(request, {
        "login_form" : login_form,
        "login_form_errors" : login_form_errors,
        "register_form" : register_form,
        "next_url" : next_url,
    }))

def logout(request):
    """Custom method to logout a user.

    The reason to use a custom logout method is just to provide a login and a
    logoutmethod on one place.
    """
    from django.contrib.auth import logout
    logout(request)

    redirect_to = '/'
    return set_message_cookie(redirect_to, msg = u"You have been logged out.")

@login_required
def password(request, template_name="user/password.html"):
    """Changes the password of current user.
    """
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            redirect_to = reverse("scipycon_account")
            return set_message_cookie(redirect_to,
                    msg = u"Your password has been changed.")
    else:
        form = PasswordChangeForm(request.user)

    return render_to_response(template_name, RequestContext(request, {
        "form" : form
    }))

@login_required
def username(request, template_name="user/username.html"):
    """Saves the username from the data form.
    """
    if request.method == "POST":
        username_form = UsernameForm(initial={"username" : request.user.username}, data=request.POST)
        if username_form.is_valid():
            request.user.username = username_form.cleaned_data.get("username")
            request.user.save()
            redirect_to = reverse("scipycon_account")
            return set_message_cookie(redirect_to,
                    msg = u"Your username has been changed.")
    else:        
        username_form = UsernameForm(initial={"username" : request.user.username})

    return render_to_response(template_name, RequestContext(request, {
        "form": username_form
    }))


def get_usernames(request):
    """Returns in json the list of ten possible usernames
    starting with the last pattern in the comma separated string
    """

    get_params = request.GET
    authors_str = get_params.get('input')

    if not authors_str:
        return HttpResponse(json.dumps(''))

    authors = authors_str.split(',')
    search_author = authors[-1].strip()

    users = User.objects.filter(
        Q(username__istartswith=search_author) | Q(
        first_name__istartswith=search_author) | Q(
        last_name__istartswith=search_author))

    results = [{'id': '',
                'info': 'plugin_header',
                'value': 'User Names'
              }]
    
    for user in users:
        results.append(
            {'id': 'author_name',
             'info': str(user.get_full_name()),
             'value': str(user.username)
            })

    json_response = {'results': results}

    return HttpResponse(json.dumps(json_response))