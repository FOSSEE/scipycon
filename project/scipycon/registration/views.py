from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.template import RequestContext

from project.scipycon.base.models import Event
from project.scipycon.registration.forms import RegistrationEditForm
from project.scipycon.registration.forms import RegistrationSubmitForm
from project.scipycon.registration.forms import AccommodationForm
from project.scipycon.registration.forms import PaymentForm
from project.scipycon.registration.forms import WifiForm
from project.scipycon.registration.models import Accommodation
from project.scipycon.registration.models import Payment
from project.scipycon.registration.models import Registration
from project.scipycon.registration.models import Wifi
from project.scipycon.registration.utils import send_confirmation
from project.scipycon.user.forms import RegistrantForm
from project.scipycon.user.models import UserProfile
from project.scipycon.user.utils import scipycon_createregistrant
from project.scipycon.utils import set_message_cookie


REG_TOTAL = 1000


@login_required
def registrations(request, scope, 
                  template_name='registration/registrations.html'):
    """Simple page to count registrations"""

    registrations = Registration.objects.all().count()

    user = request.user
    if user.is_authenticated():
        registration = Registration.objects.get(registrant=user)
    else:
        registration = None

    event = Event.objects.get(scope=scope)

    return render_to_response(template_name, RequestContext(request, {
        'params': {'scope': scope},
        'over_reg' : registrations >= REG_TOTAL and True or False,
        'registrations' : registrations,
        'registration': registration,
        'event': event}))

@login_required
def edit_registration(request, scope, id,
                      template_name='registration/edit-registration.html'):
    """Allows users that submitted a registration to edit it.
    """

    scope_entity = Event.objects.get(scope=scope)

    reg = Registration.objects.get(pk=id)
    wifi = Wifi.objects.get(user=reg.registrant)

    # TODO: This is an ugly hack to add accommodation and payment forms
    # details at later stage for SciPy.in 2010. This must be removed for
    # SciPy.in 2011
    acco, acco_created = Accommodation.objects.get_or_create(
        user=reg.registrant, scope=scope_entity)
    payment, payment_created = Payment.objects.get_or_create(
        user=reg.registrant, scope=scope_entity)

    if reg.registrant != request.user:
        redirect_to = reverse('scipycon_account', kwargs={'scope': scope})

        return set_message_cookie(
            redirect_to,
            msg = u'Redirected because the registration you selected' \
                      + ' is not your own.')

    if request.method == 'POST':
        registration_form = RegistrationEditForm(data=request.POST)
        wifi_form = WifiForm(data=request.POST)
        acco_form = AccommodationForm(data=request.POST)
        payment_form = PaymentForm(data=request.POST)

        if (registration_form.is_valid() and wifi_form.is_valid() and
            acco_form.is_valid() and payment_form.is_valid()):
            reg.organisation = registration_form.data.get('organisation')
            reg.occupation = registration_form.data.get('occupation')
            reg.city = registration_form.data.get('city')
            reg.phone_num = registration_form.data.get('phone_num')
            reg.postcode = registration_form.data.get('postcode')
            #reg.tshirt = registration_form.data.get('tshirt')
            reg.allow_contact = registration_form.data.get(
                'allow_contact') and True or False
            reg.conference = registration_form.data.get(
                'conference') and True or False
            reg.tutorial = registration_form.data.get(
                'tutorial') and True or False
            reg.sprint = registration_form.data.get(
                'sprint') and True or False
            reg.save()

            wifi = wifi_form.save(reg.registrant, reg.scope)
            acco = acco_form.save(reg.registrant, reg.scope)
            payment = payment_form.save(reg.registrant, reg.scope)

            # Saved.. redirect
            redirect_to = reverse('scipycon_account', kwargs={'scope': scope})

            return set_message_cookie(redirect_to,
                msg = u'Your changes have been saved.')
    else:
        registration_form = RegistrationEditForm(initial={
            'id' : id,
            'organisation' : reg.organisation,
            'occupation' : reg.occupation,
            'city' : reg.city,
            'phone_num': reg.phone_num,
            #'tshirt' : reg.tshirt,
            'conference': reg.conference,
            'tutorial': reg.tutorial,
            'postcode' : reg.postcode,
            'sprint' : reg.sprint,
            'allow_contact' : reg.allow_contact,
            })
        wifi_form = WifiForm(initial={
            'user': wifi.user,
            'scope': wifi.scope,
            'wifi': wifi.wifi
            })
        acco_form = AccommodationForm(initial={
            'user': acco.user,
            'scope': acco.scope,
            'sex': acco.sex,
            'accommodation_required': acco.accommodation_required,
            'accommodation_days': acco.accommodation_days,
            })
        payment_form = PaymentForm(initial={
            'user': payment.user,
            'scope': payment.scope,
            'paid': payment.type or payment.details,
            'type': payment.type,
            'details': payment.details,
            })

    return render_to_response(
        template_name, RequestContext(request, {
        'params': {'scope': scope},
        'registration': {'id': id},
        'registration_form': registration_form,
        'wifi_form': wifi_form,
        'acco_form': acco_form,
        'payment_form': payment_form}))

def submit_registration(request, scope,
        template_name='registration/submit-registration.html'):
    """Allows user to edit registration
    """

    user = request.user
    reg_count = Registration.objects.all().count()

    scope_entity = Event.objects.get(scope=scope)

    if user.is_authenticated():
        try:
            profile = user.get_profile()
        except:
            profile, new = UserProfile.objects.get_or_create(
                user=user, scope=scope_entity)
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
        acco_form = AccommodationForm(data=request.POST)
        payment_form = PaymentForm(data=request.POST)

        if request.POST.get('action', None) == 'login':
            login_form = AuthenticationForm(data=request.POST)
            if login_form.is_valid():

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
                newuser = scipycon_createregistrant(
                    request, registrant_form.data, scope)

                # Log in user
                passwd = User.objects.make_random_password()
                newuser.set_password(passwd)
                newuser.save()

                user = authenticate(username=newuser.username, password=passwd)

                login(request, user)

                newuser = user

        else:
            newuser = user

        if (registration_form.is_valid() and newuser and wifi_form.is_valid()
            and acco_form.is_valid() and payment_form.is_valid()):
            allow_contact = registration_form.cleaned_data.get(
                'allow_contact') and True or False
            conference = registration_form.cleaned_data.get(
                'conference') and True or False
            tutorial = registration_form.cleaned_data.get('tutorial') and \
                True or False
            sprint = registration_form.cleaned_data.get('sprint') and \
                True or False

            registrant = User.objects.get(pk=newuser.id)

            reg = Registration(
                scope=scope_entity,
                registrant = registrant,
                organisation = registration_form.cleaned_data.get(
                    'organisation'),
                occupation = registration_form.cleaned_data.get('occupation'),
                city = registration_form.cleaned_data.get('city'),
                #tshirt = registration_form.data.get('tshirt'),
                postcode = registration_form.cleaned_data.get('postcode'),
                phone_num = registration_form.cleaned_data.get('phone_num'),
                allow_contact = allow_contact,
                conference = conference,
                tutorial = tutorial,
                sprint = sprint)
            reg.save() 

            # get id and use as slug and invoice number
            id = reg.id
            slug = 'SCIPYIN2010%04d' % id
            reg.slug = slug
            reg.save()

            wifi = wifi_form.save(registrant, scope_entity)
            acco = acco_form.save(registrant, scope_entity)
            payment = payment_form.save(registrant, scope_entity)

            send_confirmation(registrant, scope_entity,password=passwd)

            redirect_to = reverse('scipycon_registrations',
                                  kwargs={'scope': scope})
            return set_message_cookie(redirect_to,
                    msg = u'Thank you, your registration has been submitted '\
                           'and an email has been sent with payment details.')

    else:
        registration_form = RegistrationSubmitForm()
        registrant_form = RegistrantForm()
        wifi_form = WifiForm()
        acco_form = AccommodationForm()
        payment_form = PaymentForm()

    login_form = AuthenticationForm()


    return render_to_response(template_name, RequestContext(request, {
        'params': {'scope': scope},
        'registration_form': registration_form,
        'registrant_form' : registrant_form,
        'over_reg' : reg_count >= REG_TOTAL and True or False,
        'acco_form': acco_form,
        'payment_form': payment_form,
        'wifi_form' : wifi_form,
        'message' : message,
        'login_form' : login_form
    }))


@login_required
def regstats(request, scope,
             template_name='registration/regstats.html'):
    """View that gives the statistics of registrants.
    """

    if not request.user.is_staff:
        redirect_to = reverse('scipycon_login', kwargs={'scope': scope})
        return set_message_cookie(
            redirect_to, msg = u'You must be a staff on this website to '
            'access this page.')

    q = Registration.objects.all()
    conf_num = q.filter(conference=True).count()
    tut_num = q.filter(tutorial=True).count()
    sprint_num = q.filter(sprint=True).count()

    return render_to_response(template_name, RequestContext(request,
        {'params': {'scope': scope},
         'conf_num': conf_num, 
         'tut_num': tut_num,
         'sprint_num': sprint_num,
         }))


@login_required
def manage_payments(request, scope,
                    template_name='registration/manage_payments.html'):
    """View that gives a form to manage payments.
    """

    if not request.user.is_superuser:
        redirect_to = reverse('scipycon_login', kwargs={'scope': scope})
        return set_message_cookie(
            redirect_to, msg = u'You must be an admin on this website to '
            'access this page.')

    message = None

    scope_entity = Event.objects.get(scope=scope)

    if request.method == 'POST':
        post_data = request.POST
        list_user_ids = []
        for user_id_string in post_data:
            id_str_list = user_id_string.split('_')
            if (len(id_str_list) == 3 and id_str_list[0] == 'registrant' and
              id_str_list[1] == 'id'):
                id = int(id_str_list[2])
                reg_user = User.objects.get(pk=id)

                payment, created = reg_user.payment_set.get_or_create(
                  user=reg_user, scope=scope_entity)

                payment.confirmed = True
                payment.save()

                list_user_ids.append(id)

        # This is done to unset for the confirmation for users for whom
        # mistakenly confirmation was set.
        # (TODO) This is a very expensive operation, any better solution
        # will be appreciated.
        unpaid_users = User.objects.exclude(pk__in=list_user_ids)
        for user in unpaid_users:
            payment, created = user.payment_set.get_or_create(
              user=user, scope=scope_entity)
            payment.confirmed = False
            payment.save()

    registrants = Registration.objects.all()

    return render_to_response(template_name, RequestContext(request,
        {'params': {'scope': scope},
         'registrants': registrants,
         }))
