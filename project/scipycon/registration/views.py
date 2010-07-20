import cStringIO as StringIO
import csv

from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.http import HttpResponse

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from project.scipycon.utils import set_message_cookie
from project.scipycon.user.models import UserProfile
from project.scipycon.user.utils import scipycon_createregistrant
from project.scipycon.user.forms import RegistrantForm
from project.scipycon.talk.models import Talk

from project.scipycon.registration.models import Registration
from project.scipycon.registration.forms import RegistrationSubmitForm
from project.scipycon.registration.forms import RegistrationEditForm
from project.scipycon.registration.forms import RegistrationAdminSelectForm
from project.scipycon.registration.forms import WifiForm
from project.scipycon.registration.utils import send_confirmation

from .forms import IC

REG_TOTAL = 1000


def registrations(request, scope, 
                  template_name='registration/registrations.html'):
    """Simple page to count registrations"""

    registrations = Registration.objects.all().count()
    return render_to_response(template_name, RequestContext(request, {
        'params': {'scope': scope},
        'over_reg' : registrations >= REG_TOTAL and True or False,
        'registrations' : registrations}))

@login_required
def edit_registration(request, scope, id,
                      template_name='registration/edit-registration.html'):
    """Allows users that submitted a registration to edit it.
    """

    reg = Registration.objects.get(pk=id)

    if reg.registrant != request.user:
        redirect_to = reverse('scipycon_account', kwargs={'scope': scope})

        return set_message_cookie(
            redirect_to,
            msg = u'Redirected because the registration you selected' \
                      + ' is not your own.')

    if request.method == 'POST':
        form = RegistrationEditForm(data=request.POST)
        if form.is_valid():
            reg.organisation = form.data.get('organisation')
            reg.occupation = form.data.get('occupation')
            reg.city = form.data.get('city')
            reg.tshirt = form.data.get('tshirt')
            reg.allow_contact = form.data.get('allow_contact') and True or False
            reg.conference = form.data.get('conference') and True or False
            reg.tutorial = form.data.get('tutorial') and True or False
            reg.sprint = form.data.get('sprint') and True or False
            reg.save()

            # Saved.. redirect
            redirect_to = reverse('scipycon_account', kwargs={'scope': scope})

            return set_message_cookie(redirect_to,
                msg = u'Your changes have been saved.')
    else:
        form = RegistrationEditForm(initial={
                                    'id' : id,
                                    'organisation' : reg.organisation,
                                    'occupation' : reg.occupation,
                                    'city' : reg.city,
                                    'tshirt' : reg.tshirt,
                                    'conference': reg.conference,
                                    'tutorial': reg.tutorial,
                                    'postcode' : reg.postcode,
                                    'sprint' : reg.sprint,
                                    'allow_contact' : reg.allow_contact,
            })

    return render_to_response(
        template_name, RequestContext(request, {
        'params': {'scope': scope}}))

def submit_registration(request, scope,
        template_name='registration/submit-registration.html'):
    """Allows user to edit registration
    """

    user = request.user
    reg_count = Registration.objects.all().count()

    if user.is_authenticated():
        try:
            profile = user.get_profile()
        except:
            profile, new = UserProfile.objects.get_or_create(user=user)
            if new:
                profile.save()
        try:
            registration = Registration.objects.get(registrant=user)
            if registration:
                redirect_to = reverse('scipycon_account',
                                      kwargs={'scope': scope})
                return set_message_cookie(
                    redirect_to, msg = u'You have already been registered.')

        except ObjectDoesNotExist:
            pass

    message = None

    if request.method == 'POST':
        registration_form = RegistrationSubmitForm(data=request.POST)
        registrant_form = RegistrantForm(data=request.POST)
        wifi_form = WifiForm(data=request.POST)

        if request.POST.get('action', None) == 'login':
            login_form = AuthenticationForm(data=request.POST)
            if login_form.is_valid():

                from django.contrib.auth import login
                login(request, login_form.get_user())

                redirect_to = reverse('scipycon_submit_registration',
                                      kwargs={'scope': scope})
                return set_message_cookie(redirect_to,
                        msg = u'You have been logged in please continue' + \
                               'with registration.')

        newuser = None
        passwd = None
        if not user.is_authenticated():
            if registrant_form.is_valid():
                newuser = scipycon_createregistrant(request, registrant_form.data)
                # Log in user
                passwd = User.objects.make_random_password()
                newuser.set_password(passwd)
                newuser.save()
                from django.contrib.auth import authenticate
                user = authenticate(username=newuser.username, password=passwd)

                login(request, user)

                newuser = user

        else:
            newuser = user

        if registration_form.is_valid() and newuser:
            allow_contact = registration_form.data.get('allow_contact') and \
                True or False
            conference = registration_form.data.get('conference') and \
                True or False
            tutorial = registration_form.data.get('tutorial') and \
                True or False
            sprint = registration_form.data.get('sprint') and \
                True or False

            registrant = User.objects.get(pk=newuser.id)

            presenter = None
            talks = Talk.objects.filter(
                speaker=registrant).filter(approved=True)
            if talks:
                for talk in talks:
                    if talk.duration == '30':
                        presenter = True
                    elif talk.duration == '60':
                        presenter = True
            
            reg = Registration(
                    #     slug = newuser.username,
                registrant = registrant,
                organisation = registration_form.data.get('organisation'),
                occupation = registration_form.data.get('occupation'),
                city = registration_form.data.get('city'),
                tshirt = registration_form.data.get('tshirt'),
                postcode = registration_form.cleaned_data.get('postcode'),
                allow_contact = allow_contact,
                conference = conference,
                tutorial = tutorial,
                sprint = sprint)
            reg.save() 

            # get id and use as slug and invoice number
            id = reg.id
            slug = 'SPYIN10%03d' % id
            reg.slug = slug
            reg.save()

            # additional tasks:
            if wifi_form.is_valid():
                wifi = wifi_form.save(registrant)
            
            # 1. include random password if we are a new user
            if passwd:
                send_confirmation(registrant, slug, password=passwd)
            else:
            # 2. send user email with registration id
                send_confirmation(registrant, slug)

            redirect_to = reverse('scipycon_registrations',
                                  kwargs={'scope': scope})
            return set_message_cookie(redirect_to,
                    msg = u'Thank you, your registration has been submitted '\
                           'and an email has been sent with payment details.')

    else:
        registration_form = RegistrationSubmitForm()
        registrant_form = RegistrantForm()
        wifi_form = WifiForm()

    login_form = AuthenticationForm()


    return render_to_response(template_name, RequestContext(request, {
        'params': {'scope': scope},
        'registration_form': registration_form,
        'registrant_form' : registrant_form,
        'over_reg' : reg_count >= REG_TOTAL and True or False,
        'wifi_form' : wifi_form,
        'message' : message,
        'login_form' : login_form
    }))
