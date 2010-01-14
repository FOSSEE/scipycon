# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render_to_response
from django.template import RequestContext

from project.kiwipycon.user.forms import RegisterForm
from project.kiwipycon.proceedings.forms import ProceedingsForm


@login_required
def submit(request, template = 'proceedings/submit.html'):
    """View to submit the proceedings paper.
    """
    user = request.user
    if user.is_authenticated():
        try:
            profile = user.get_profile()
        except:
            profile, new = UserProfile.objects.get_or_create(user=user)
            if new:
                profile.save()
    message = None

    if request.method == 'POST':
        proceedings_form = ProceedingsForm(data=request.POST)

        register_form = RegisterForm(data=request.POST,
                                        files=request.FILES)

        if request.POST.get('action', None) == 'login':
            login_form = AuthenticationForm(data=request.POST)
            if login_form.is_valid():

                from django.contrib.auth import login
                login(request, login_form.get_user())

                redirect_to = reverse('kiwipycon_submit_proceedings')
                return set_message_cookie(redirect_to,
                        msg = u'You have been logged in.')

        if request.POST.get('action', None) == 'register':
            # add the new user
            if register_form.is_valid():

                user = kiwipycon_createuser(request, register_form.data)

        if proceedings_form.is_valid():
            if user.is_authenticated():
                title = proceedings_form.data.get('title')

                # Saved, ... redirect back to account
                redirect_to = reverse('kiwipycon_account')
                return set_message_cookie(redirect_to,
                        msg = u'Thanks, your paper has been submitted.')
            else:
                redirect_to = reverse('kiwipycon_submit_proceedings')
                return set_message_cookie(redirect_to,
                        msg = u'Something is wrong here.')

    else:
        proceedings_form = ProceedingsForm()
        register_form = RegisterForm()
    login_form = AuthenticationForm()

        
    proceedings_form = ProceedingsForm()
    register_form = RegisterForm()
    login_form = AuthenticationForm()

    context = RequestContext(request, {
        'proceedings_form': proceedings_form,
        'register_form' : register_form,
        'message' : message,
        'login_form' : login_form
        })

    return render_to_response(template, context)


def edit(request, id, template = 'proceedings/edit.html'):
    """View to edit the proceedings paper.
    """

    context = RequestContext(request, {
        'proceedings_form': proceedings_form,
        'register_form' : register_form,
        'message' : message,
        'login_form' : login_form
        })

    return render_to_response(template, context)
