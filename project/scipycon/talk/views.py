from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic.list_detail import object_list
from django.views.generic.list_detail import object_detail

from PIL import Image

from tagging.models import Tag

from project.scipycon.talk.models import Talk
from project.scipycon.talk.forms import TalkSubmitForm
from project.scipycon.talk.forms import TalkEditForm
from project.scipycon.talk.models import DURATION_CHOICES
from project.scipycon.talk.models import AUDIENCE_CHOICES
from project.scipycon.utils import set_message_cookie
from project.scipycon.utils import slugify
from project.scipycon.user.models import UserProfile
from project.scipycon.user.forms import RegisterForm
from project.scipycon.user.utils import scipycon_createuser


def list_talks(request, scope):
    objects = Talk.objects.filter(approved=True)
    extra_context = dict(count=objects.count())
    return object_list(request, objects, extra_context=extra_context)

def talk(request, scope, id):
    objects = Talk.objects.filter(approved=True)
    audience = {}
    for choice in AUDIENCE_CHOICES:
        audience[choice[0]] = choice[1]
    extra_context = dict(choices=audience)
    return object_detail(request, objects, id, extra_context=extra_context)

@login_required
def edit_talk(request, scope, id, template_name='talk/edit-talk.html'):
    """Allows users that submitted a talk to edit it until the talk is approved.
    """

    talk = Talk.objects.get(pk=id)

    if talk.approved == True:
        redirect_to = reverse('scipycon_account', kwargs={'scope': scope})
        return set_message_cookie(redirect_to,
                msg = u'Sorry but you cannot edit the talk once'\
                      + ' it has been accepted.')

    if talk.speaker != request.user:
        redirect_to = reverse('scipycon_account', kwargs={'scope': scope})
        return set_message_cookie(redirect_to,
                msg = u'Redirected to account because the talk you selected' \
                      + ' is not your own.')

    if request.method == 'POST':
        form = TalkEditForm(data=request.POST)
        if form.is_valid():
            talk.slug = slugify(form.data.get('title'))
            talk.authors_bio = form.data.get('authors_bio')
            talk.contact = form.data.get('contact')
            talk.title = form.data.get('title')
            talk.abstract = form.data.get('abstract')
#            talk.outline = form.data.get('outline')
            talk.topic = form.data.get('topic')
#            talk.topic_other = form.data.get('topic_other')
            talk.duration = form.data.get('duration')
            talk.audience = form.data.get('audience')
#            talk.audience_other = form.data.get('audience_other')
#            talk.tags = form.data.get('tags')
            talk.save()
            # Saved.. redirect
            redirect_to = reverse('scipycon_account', kwargs={'scope': scope})
            return set_message_cookie(redirect_to,
                    msg = u'Your changes have been saved.')
    else:
        form = TalkEditForm(initial={
                                    'id' : id,
                                    'authors_bio' : talk.authors_bio,
                                    'contact' : talk.contact,
                                    'title' : talk.title,
                                    'abstract' : talk.abstract,
#                                    'outline' : talk.outline,
                                    'topic' : talk.topic,
#                                    'topic_other' : talk.topic_other,
                                    'duration' : talk.duration,
                                    'audience' : talk.audience,
#                                    'audience_other' : talk.audience_other,
#                                    'tags' : talk.tags,
            })

    return render_to_response(template_name, RequestContext(request, locals()))

@login_required()
def submit_talk(request, scope, template_name='talk/submit-talk.html'):
    """Allows user to edit profile
    """

    from project.scipycon.base.models import Event

    user = request.user
    if user.is_authenticated():
        try:
            profile = user.get_profile()
        except:
            scope_entity = Event.objects.get(scope=scope)

            profile, new = UserProfile.objects.get_or_create(
                user=user, scope=scope_entity)
            if new:
                profile.save()

    message = None

    if request.method == 'POST':
        talk_form = TalkSubmitForm(data=request.POST)

        register_form = RegisterForm(data=request.POST, files=request.FILES)

        if request.POST.get('action', None) == 'login':
            login_form = AuthenticationForm(data=request.POST)
            if login_form.is_valid():

                from django.contrib.auth import login
                login(request, login_form.get_user())

                redirect_to = reverse('scipycon_submit_talk',
                                      kwargs={'scope': scope})
                return set_message_cookie(redirect_to,
                        msg = u'You have been logged in.')

        if request.POST.get('action', None) == 'register':
            # add the new user
            if register_form.is_valid():

                user = scipycon_createuser(request, register_form.data)

        if talk_form.is_valid():
            if user.is_authenticated():
                title = talk_form.data.get('title')
                talk = Talk.objects.create(
                    slug = slugify(title),
                    speaker = User.objects.get(pk=user.id),
                    authors_bio = talk_form.data.get('authors_bio'),
                    contact = talk_form.data.get('contact'),
                    title = talk_form.data.get('title'),
                    abstract = talk_form.data.get('abstract'),
                    topic = talk_form.data.get('topic'),
                    duration = talk_form.data.get('duration'),
                    audience = talk_form.data.get('audience'),
                    approved = False,
#                    tags = talk_form.data.get('tags')
                    )
                talk.save()
                # Saved, ... redirect back to account
                redirect_to = reverse('scipycon_account',
                                      kwargs={'scope': scope})
                return set_message_cookie(redirect_to,
                        msg = u'Thanks, your talk has been submitted.')
            else:
                redirect_to = reverse('scipycon_submit_talk',
                                      kwargs={'scope': scope})
                return set_message_cookie(redirect_to,
                        msg = u'Something is wrong here.')

    else:
        talk_form = TalkSubmitForm()
        register_form = RegisterForm()
    login_form = AuthenticationForm()


    return render_to_response(template_name, RequestContext(request, {
        'talk_form': talk_form,
        'register_form' : register_form,
        'message' : message,
        'login_form' : login_form
    }))

def list_talks(request, scope, template_name='talk/list-all-talks.html'):
    """List all the tasks submitted by a user.
    """

    talks = Talk.objects.filter(approved=True)

    return render_to_response(template_name, RequestContext(request, {
        'talk_list': talks,
    }))
