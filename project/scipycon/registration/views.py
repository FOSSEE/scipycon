import cStringIO as StringIO
import csv

from django.conf import settings
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
from project.scipycon.utils import slugify
from project.scipycon.user.models import UserProfile
from project.scipycon.user.utils import scipycon_createregistrant
from project.scipycon.user.forms import RegistrantForm
from project.scipycon.talk.models import Talk

from .models import Registration
from .models import Wifi
from .forms import RegistrationSubmitForm
from .forms import RegistrationEditForm
from .forms import RegistrationAdminSelectForm
from .forms import WifiForm
from .utils import send_confirmation

from .forms import IC

REG_TOTAL = 1000

@login_required
def download_csv(request, scope,
        template_name = 'registration/download-csv.html'):
    """
    """
    if not request.user.is_staff:
        redirect_to = reverse('scipycon_login')
    if request.method == "POST":
        form = RegistrationAdminSelectForm(request.POST)
        if form.is_valid():
            conference = form.cleaned_data['by_conference']
            tutorial = form.cleaned_data['by_tutorial']
            sprint = form.cleaned_data['by_sprint']
            amount = form.cleaned_data['by_amount']
            tshirt = form.cleaned_data['by_tshirt']
            order_by = form.cleaned_data['order_by']
            include = form.cleaned_data['include']
            q = Registration.objects.all()
            if conference == 'conference':
                q = q.filter(conference=True)
            elif conference == 'no conference':
                q = q.filter(conference=False)
            elif tutorial == 'tutorial':
                q = q.filter(tutorial=True)
            elif tutorial == 'no tutorial':
                q = q.filter(tutorial=False)
            if sprint == 'sprint':
                q = q.filter(sprint=True)
            if sprint == 'no sprint':
                q = q.filter(sprint=False)
            elif tshirt != 'all':
                q = q.filter(tshirt=tshirt)
            q = q.order_by('registrant__email')
            query = q.query
            results = list(q)
            if include == []:
                # default to include all fields
                include = [i[0] for i in IC]
            if results:
                response = HttpResponse(mimetype='text/csv')
                response['Content-Disposition'] = 'attachment; filename=registrations.csv'
                output = csv.writer(response)
                output.writerow([h for h in include])
                for row in results:
                    conference = row.conference == True and 'yes' or 'no'
                    tutorial = row.tutorial == True and 'yes' or 'no'
                    sprint = row.sprint == True and 'yes' or 'no'
                    wrow = []
                    if 'Name' in include:
                        wrow.append(
                            row.registrant.get_full_name().encode('utf-8'))
                    if 'Email' in include:
                        wrow.append(row.registrant.email.encode('utf-8'))
                    if 'Organisation' in include:
                        wrow.append(row.organisation.encode('utf-8'))
                    if 'Conference' in include:
                        wrow.append(conference)
                    if 'Tutorial' in include:
                        wrow.append(tutorial)
                    if 'Sprint' in include:
                        wrow.append(sprint)
                    if 'T-size' in include:
                        wrow.append(row.tshirt)
                    output.writerow(wrow)
                return response
            else:
                no_results = u'No results found for the query'

    else:
        form = RegistrationAdminSelectForm()
    return render_to_response(template_name, RequestContext(request,
        locals()))

# NOT REQUIRED FOR SciPy.in
@login_required
def invoice(request, scope, template_name='registration/invoice.html'):
    user = request.user
    registration = get_object_or_404(Registration, registrant=user)
    if registration.sponsor:
        redirect_to = reverse('scipycon_account')
        return set_message_cookie(redirect_to,
                msg = u'You are a sponsored guest, no payment required.')
    return render_to_response(template_name, RequestContext(request,
        {'registration' : registration, 'user': user}))

@login_required
def pdf_invoice(request, scope, template_name='registration/invoice.html'):
    user = request.user
    registration = get_object_or_404(Registration, registrant=user)
    if registration.sponsor:
        redirect_to = reverse('scipycon_account')
        return set_message_cookie(redirect_to,
                msg = u'You are a sponsored guest, no payment required.')
    content = render_to_string(template_name,
        {'registration' : registration, 'user': user})
    result = StringIO.StringIO()
    import ho.pisa
    pdf = ho.pisa.pisaDocument(StringIO.StringIO(content.encode("UTF-8")),result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), mimetype='application/pdf')
    return HttpResponse("Gremlins ate your invoice, please try html" \
        " version")


def registrations(request, scope,
        template_name='registration/registrations.html'):
    """Simple page to count registrations"""
    #registrations = Registration.objects.filter(payment=True).count()
    registrations = Registration.objects.all().count()
    return render_to_response(template_name, RequestContext(request,
        {
        'over_reg' : registrations >= REG_TOTAL and True or False,
            'registrations' : registrations}))

@login_required
def edit_registration(request, scope, id,
        template_name='registration/edit-registration.html'):
    '''Allows users that submitted a registration to edit it.
    '''
    reg = Registration.objects.get(pk=id)

    if reg.registrant != request.user:
        redirect_to = reverse('scipycon_account')
        return set_message_cookie(redirect_to,
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
            redirect_to = reverse('scipycon_account')
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
    '''Allows user to edit registration
    '''
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
                redirect_to = reverse('scipycon_account')
                return set_message_cookie(redirect_to,
                        msg = u'You have already been registered.')

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

                redirect_to = reverse('scipycon_submit_registration')
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

                from django.contrib.auth import login
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
            slug = 'KPC09%03d' % id
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

            redirect_to = reverse('scipycon_registrations')
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
