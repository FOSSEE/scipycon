import csv
import datetime
import time

from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import loader
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

    reg = Registration.objects.get(pk=int(id))
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
            'wifi': wifi.wifi,
            'registration_id': wifi.registration_id
            })
        acco_form = AccommodationForm(initial={
            'user': acco.user,
            'scope': acco.scope,
            'sex': acco.sex,
            'accommodation_required': acco.accommodation_required,
            'accommodation_on_1st': acco.accommodation_on_1st,
            'accommodation_on_2nd': acco.accommodation_on_2nd,
            'accommodation_on_3rd': acco.accommodation_on_3rd,
            'accommodation_on_4th': acco.accommodation_on_4th,
            'accommodation_on_5th': acco.accommodation_on_5th,
            'accommodation_on_6th': acco.accommodation_on_6th,
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

            send_confirmation(registrant, scope_entity, password=passwd)

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

    reg_q = Registration.objects.all()
    conf_num = reg_q.filter(conference=True).count()
    tut_num = reg_q.filter(tutorial=True).count()
    sprint_num = reg_q.filter(sprint=True).count()

    acco_q = Accommodation.objects.all()
    male = acco_q.filter(sex='Male').count()
    female = acco_q.filter(sex='Female').count()

    # Day 1 details
    day1 = acco_q.filter(accommodation_on_1st=True)
    acco_1 = {
       'total': day1.count(),
       'male': day1.filter(sex='Male').count(),
       'female': day1.filter(sex='Female').count()
       }

    # Day 2 details
    day2 = acco_q.filter(accommodation_on_2nd=True)
    acco_2 = {
       'total': day2.count(),
       'male': day2.filter(sex='Male').count(),
       'female': day2.filter(sex='Female').count()
       }

    # Day 3 details
    day3 = acco_q.filter(accommodation_on_3rd=True)
    acco_3 = {
       'total': day3.count(),
       'male': day3.filter(sex='Male').count(),
       'female': day3.filter(sex='Female').count()
       }

    # Day 4 details
    day4 = acco_q.filter(accommodation_on_4th=True)
    acco_4 = {
       'total': day4.count(),
       'male': day4.filter(sex='Male').count(),
       'female': day4.filter(sex='Female').count()
       }


    # Day 5 details
    day5 = acco_q.filter(accommodation_on_5th=True)
    acco_5 = {
       'total': day5.count(),
       'male': day5.filter(sex='Male').count(),
       'female': day5.filter(sex='Female').count()
       }

    # Day 6 details
    day6 = acco_q.filter(accommodation_on_6th=True)
    acco_6 = {
       'total': day6.count(),
       'male': day6.filter(sex='Male').count(),
       'female': day6.filter(sex='Female').count()
       }

    return render_to_response(template_name, RequestContext(request,
        {'params': {'scope': scope},
         'conf_num': conf_num, 
         'tut_num': tut_num,
         'sprint_num': sprint_num,
         'male': male,
         'female':female,
         'acco_days': [acco_1, acco_2, acco_3, acco_4, acco_5, acco_6],
         }))

@login_required
def regstats_download(request, scope):
    """Sends a downloadable PDF for registration statistics
    """

    if not request.user.is_staff:
        redirect_to = reverse('scipycon_login')
        return HttpResponseRedirect(redirect_to)

    filename = 'regstats%s.csv' % datetime.datetime.strftime(
      datetime.datetime.now(), '%Y%m%d%H%M%S')

    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename=%s' % (
      filename)

    output = csv.writer(response)

    output.writerow(['Name', 'Gender', 'City',
                     'Registration Fees Paid',
                     'Attending Conference',
                     'Attending Tutorial',
                     'Attending Sprint',
                     'Laptop Identification Number',
                     'Accommodation Fees Paid',
                     'Accommodation on 12th night',
                     'Accommodation on 13th night',
                     'Accommodation on 14th night',
                     'Accommodation on 15th night',
                     'Accommodation on 16th night',
                     'Accommodation on 17th night'])

    regs = Registration.objects.order_by(
      'registrant__first_name', 'registrant__last_name')
    for reg in regs:
        row = []

        payment, create = reg.registrant.payment_set.get_or_create(
          user=reg.registrant, scope=reg.scope)
        acco, created = reg.registrant.accommodation_set.get_or_create(
          user=reg.registrant, scope=reg.scope)
        wifi, create = reg.registrant.wifi_set.get_or_create(
          user=reg.registrant, scope=reg.scope)

        row.append('"%s"' % reg.registrant.get_full_name())
        row.append(acco.sex)
        row.append(reg.city)
        row.append('Yes' if payment.confirmed else 'No')
        row.append('Yes' if reg.conference else 'No')
        row.append('Yes' if reg.tutorial else 'No')
        row.append('Yes' if reg.sprint else 'No')
        row.append(wifi.registration_id)
        row.append('Yes' if payment.acco_confirmed
           else 'No')
        row.append('Yes' if acco.accommodation_on_1st else 'No')
        row.append('Yes' if acco.accommodation_on_2nd else 'No')
        row.append('Yes' if acco.accommodation_on_3rd else 'No')
        row.append('Yes' if acco.accommodation_on_4th else 'No')
        row.append('Yes' if acco.accommodation_on_5th else 'No')
        row.append('Yes' if acco.accommodation_on_6th else 'No')
        output.writerow(row)

    #output.writerow()
    return response


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

        mail_subject = 'SciPy.in 2010: Confirmation of fee payment'
        mail_template = 'notifications/payment_confirmation2010.html'

        def parse_form():
            """Helper function that gets the User ID from the
            form name
            """

            confirmed_ids = []
            acco_ids = []
            date_ids = {}

            for name_string in post_data:
                id_str_list = name_string.split('_')
                if (len(id_str_list) == 3 and id_str_list[1] == 'id'):
                    if id_str_list[0] == 'confirmed':
                        confirmed_ids.append(int(id_str_list[2]))
                    if id_str_list[0] == 'acco':
                        acco_ids.append(int(id_str_list[2]))
                    if id_str_list[0] == 'date':
                        date_str = post_data.get(name_string, None)
                        if date_str:
                            date_ids[int(id_str_list[2])] = post_data.get(
                              name_string, '')

            return confirmed_ids, acco_ids, date_ids

        confirmed_ids, acco_ids, date_ids = parse_form()

        confirmed_users = set(User.objects.filter(id__in=confirmed_ids))
        acco_users = set(User.objects.filter(id__in=acco_ids))

        # Users for whom both registration and accommodation is confirmed
        for user in confirmed_users & acco_users:
            payment, created = user.payment_set.get_or_create(
              user=user, scope=scope_entity)

            payment.confirmed = True
            payment.acco_confirmed = True
            payment.save()

            if not payment.confirmed_mail and not payment.acco_confirmed_mail:
                mail_message = loader.render_to_string(
                  mail_template,
                  dictionary={'name': user.get_full_name(),
                            'acco': True,
                            'reg': True})
                user.email_user(mail_subject, mail_message,
                                from_email='admin@scipy.in')
                payment.confirmed_mail =True
                payment.acco_confirmed_mail = True
                payment.save()

        # Users for whom only registration is confirmed
        for user in confirmed_users - acco_users:
            payment, created = user.payment_set.get_or_create(
              user=user, scope=scope_entity)

            payment.confirmed = True
            payment.save()

            if not payment.confirmed_mail:
                mail_message = loader.render_to_string(
                  mail_template,
                  dictionary={'name': user.get_full_name(),
                          'reg': True})
                user.email_user(mail_subject, mail_message,
                                from_email='admin@scipy.in')
                payment.confirmed_mail =True
                payment.save()

        # Users for whom only accommodation is confirmed
        for user in acco_users - confirmed_users:
            payment, created = user.payment_set.get_or_create(
              user=user, scope=scope_entity)

            payment.acco_confirmed = True
            payment.save()

            if not payment.acco_confirmed_mail:
                mail_message = loader.render_to_string(
                  mail_template,
                  dictionary={'name': user.get_full_name(),
                          'acco': True})
                user.email_user(mail_subject, mail_message,
                                from_email='admin@scipy.in')
                payment.acco_confirmed_mail = True
                payment.save()

        # Users for whom fee payment date is updated
        for id in date_ids:
            user = User.objects.get(id=id)
            payment, created = user.payment_set.get_or_create(
              user=user, scope=scope_entity)

            time_format = "%m/%d/%Y"
            date = datetime.datetime.fromtimestamp(time.mktime(
              time.strptime(date_ids[id], time_format)))

            payment.date_confirmed = date
            payment.save()

    registrants = Registration.objects.all()

    return render_to_response(template_name, RequestContext(request,
        {'params': {'scope': scope},
         'registrants': registrants,
         }))
