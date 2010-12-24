from urlparse import urlparse

import simplejson as json
import os

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

from PIL import Image

from project.scipycon.base.models import Event
from project.scipycon.registration.models import Registration
from project.scipycon.registration.models import Wifi
from project.scipycon.registration.forms import WifiForm
from project.scipycon.talk.models import Talk
from project.scipycon.user.forms import EditProfileForm
from project.scipycon.user.forms import RegisterForm
from project.scipycon.user.forms import UsernameForm
from project.scipycon.user.utils import handle_uploaded_photo
from project.scipycon.user.utils import scipycon_createuser
from project.scipycon.utils import set_message_cookie

#User_dump Http404 Error
from django.http import Http404
#for user_dump creation
from project.scipycon.registration.models import Accommodation

#Pdf badge generation
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.platypus import  Image as reportlabImage
from django.core.exceptions import ObjectDoesNotExist


@login_required
def account(request, scope, template_name="user/account.html"):
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

    event = Event.objects.get(scope=scope)

    if profile.photo:
        photo = os.path.join(settings.USER_MEDIA_URL, profile.photo)
    else:
        photo = '/img/user-default.png'

    return render_to_response(template_name, RequestContext(request, {
        'params': {'scope': scope},
        'user' : user,
        'profile' : profile,
        'photo' : photo,
        'talks' : talks,
        'registration' : registration,
        'event': event}))

@login_required
def edit_profile(request, scope, template_name="user/editprofile.html"):
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

            redirect_to = reverse('scipycon_account',
                                  kwargs={'scope': scope})
            return set_message_cookie(redirect_to,
                    msg = u'Your profile has been changed.')

    else:
        form = EditProfileForm(
            initial={
                'email' : user.email,
                'email2' : user.email, # hidden field
                'first_name' : user.first_name,
                'last_name' : user.last_name,
                'url' : profile.url,
                'about' : profile.about,
            })

    return render_to_response(template_name, RequestContext(request, {
        'params': {'scope': scope},
        'form': form
    }))

def login(request, scope, template_name="user/login.html"):
    """Custom view to login or register/login a user.
       Integration of register and login form
       It uses Django's standard AuthenticationForm, though.
    """

    user = request.user
    if user.is_authenticated():
        redirect_to = reverse("scipycon_account", kwargs={'scope': scope})
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
                redirect_to = reverse('scipycon_account',
                                      kwargs={'scope': scope})

            from django.contrib.auth import login
            login(request, login_form.get_user())

            return set_message_cookie(redirect_to, msg = u"You have been logged in.")

    elif request.POST.get("action") == "register":
        register_form = RegisterForm(data=request.POST)
        if register_form.is_valid():

            user = scipycon_createuser(request, register_form.data, scope)

            redirect_to = request.POST.get("next")
            if not redirect_to or '//' in redirect_to or ' ' in redirect_to:
                redirect_to = reverse('scipycon_account',
                                      kwargs={'scope': scope})

            return set_message_cookie(
                redirect_to, msg = u"You have been registered and logged in.")

    # Get next_url
    next_url = request.REQUEST.get("next")
    if next_url is None:
        next_url = request.META.get("HTTP_REFERER")
    if next_url is None:
        next_url = reverse('scipycon_account', kwargs={'scope': scope})

    # Get just the path of the url.
    # See django.contrib.auth.views.login for more
    next_url = urlparse(next_url)
    next_url = next_url[2]

    try:
        login_form_errors = login_form.errors["__all__"]
    except KeyError:
        login_form_errors = None

    return render_to_response(template_name, RequestContext(request, {
        'params': {'scope': scope},
        'login_form' : login_form,
        'login_form_errors' : login_form_errors,
        'register_form' : register_form,
        'next_url' : next_url,
    }))

def logout(request, scope):
    """Custom method to logout a user.

    The reason to use a custom logout method is just to provide a login and a
    logoutmethod on one place.
    """

    from django.contrib.auth import logout
    logout(request)

    redirect_to = '/%s' % (scope)
    return set_message_cookie(redirect_to, msg = u"You have been logged out.")

@login_required
def password(request, scope, template_name='user/password.html'):
    """Changes the password of current user.
    """

    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            redirect_to = reverse('scipycon_account', kwargs={'scope': scope})
            return set_message_cookie(redirect_to,
                    msg = u'Your password has been changed.')
    else:
        form = PasswordChangeForm(request.user)

    return render_to_response(template_name, RequestContext(request, {
        'params': {'scope': scope},
        'form' : form
    }))

@login_required
def username(request, scope, template_name='user/username.html'):
    """Saves the username from the data form.
    """
    if request.method == 'POST':
        username_form = UsernameForm(
            initial={'username' : request.user.username},
            data=request.POST)
        if username_form.is_valid():
            request.user.username = username_form.cleaned_data.get("username")
            request.user.save()
            redirect_to = reverse('scipycon_account',
                                  kwargs={'scope': scope})
            return set_message_cookie(redirect_to,
                    msg = u"Your username has been changed.")
    else:        
        username_form = UsernameForm(initial={"username" : request.user.username})

    return render_to_response(template_name, RequestContext(request, {
        'params': {'scope': scope},
        'form': username_form
    }))


def get_usernames(request, scope):
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


@login_required
def get_user_dump(request, scope,template_name='user/dump.html'):
    """ Gets a general dump of user related info
    """
    print request.user.is_staff
    if request.user.is_staff:
        qs=Registration.objects.all()
        rows=[]    
        for obj in qs:
            row = {}
            row['first_name'] = obj.registrant.first_name
            row['last_name'] = obj.registrant.last_name
            try:
                accomodation_require = Accommodation.objects.filter(user__username=obj.registrant.username)[0]
                row['sex'] = accomodation_require.sex
            except:
                row['sex'] = '-'
            row['city'] = obj.city
            row['organization'] = obj.organisation
            row['occupation'] = obj.occupation
            row['conference'] = obj.conference 
            row['sprint'] = obj.sprint
            row['tutorial'] = obj.tutorial
            try:
                wifi_require = Wifi.objects.filter(user__username=obj.registrant.username)[0]
                row['wifi'] = wifi_require.wifi
            except:
                row['wifi']='Wifi Unspecified'
            rows.append(row)
        return render_to_response(template_name, RequestContext(request, {
                    'rows':  rows}))
                    

    else:
            raise Http404


@login_required
def badge(request,scope):

    from django.conf import settings

    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(mimetype='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=scipybadge.pdf'

    # Create the PDF object, using the response object as its "file."
    c = canvas.Canvas(response)

    ref=5*cm
    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    c.rect(ref,ref,9*cm,6*cm)

    img_path = os.path.join(settings.STATIC_ROOT, 'img', 'scipyshiny_small.png')
    im = reportlabImage(img_path, width=1.75*cm, height=1.75*cm)
    im.drawOn(c,(ref+0.8*cm),(ref+4.3*cm))
    c.setFont('Helvetica', 6)
    c.drawString((ref+1.0*cm),(ref+4.2*cm),'scipy.in 2010') 
    c.drawString((ref+1.1*cm),(ref+4.0*cm),'Hyderabad') 

    c.setFont('Helvetica', 14)
    print request.user.id
    reg_obj=Registration.objects.get(registrant=request.user.id)
    c.drawString((ref+3.4*cm),(ref+4.9*cm),str(reg_obj.slug)) 
    
    c.setFont('Helvetica-Bold', 15)
    c.drawString((ref+0.6*cm),(ref+3.4*cm),str(request.user.get_full_name()))
    c.setFont('Helvetica', 11)
    c.drawString((ref+2.8*cm),(ref+2.7*cm),reg_obj.organisation)
    c.setFont('Helvetica', 11)
    try:
        c.drawString((ref+2.8*cm),(ref+2.2*cm),reg_obj.occupation.split(':')[1])
    except IndexError:
        c.drawString((ref+2.8*cm),(ref+2.3*cm),reg_obj.occupation)
        
    c.setFont('Helvetica', 10)
    c.drawString((ref+2.8*cm),(ref+1.7*cm),reg_obj.city)
    c.setFont('Helvetica', 10)
    c.drawString((ref+2.8*cm),(ref+1*cm),'Participant')
    
   
    try:
        wifi_obj=Wifi.objects.get(user=request.user.id)
        c.setFont('Helvetica', 10)
        c.drawString((ref+5.6*cm),(ref+0.5*cm),wifi_obj.registration_id)
    except :
        pass

    
    # Close the PDF object cleanly, and we're done.
    c.showPage()
    c.save()
    return response
