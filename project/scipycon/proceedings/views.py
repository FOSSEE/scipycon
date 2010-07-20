import os

from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.template import RequestContext

from project.scipycon.proceedings.booklet import mk_scipy_paper
from project.scipycon.proceedings.forms import ProceedingsForm
from project.scipycon.proceedings.models import Paper
from project.scipycon.user.forms import RegisterForm
from project.scipycon.user.models import UserProfile
from project.scipycon.utils import set_message_cookie


def handleUploadedFile(proceedings_form_data, rst_file):
    """Handles the uploaded file content and process the form
    """

    title = proceedings_form_data.get('title')
    abstract = proceedings_form_data.get('abstract')
    body = proceedings_form_data.get('body')
    authors = proceedings_form_data.get('authors')

    if rst_file:
        destination = open('some/file/name.txt', 'wb+')
        for chunk in rst_file.chunks():
            destination.write(chunk)
        destination.close()

    return title, abstract, body, authors


@login_required
def submit(request, scope, id=None, template='proceedings/submit.html'):
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
        register_form = RegisterForm(data=request.POST)

        if request.POST.get('action', None) == 'login':
            login_form = AuthenticationForm(data=request.POST)
            if login_form.is_valid():

                login(request, login_form.get_user())

                redirect_to = reverse('scipycon_submit_proceedings',
                                      kwargs={'scope': scope})
                return set_message_cookie(redirect_to,
                        msg = u'You have been logged in.')

        if request.POST.get('action', None) == 'register':
            # add the new user
            if register_form.is_valid():

                user = scipycon_createuser(request, register_form.data)

        proceedings_form = ProceedingsForm(data=request.POST,
                                           files=request.FILES)
  
        if proceedings_form.is_valid():
            if user.is_authenticated():
                # Data from reSt file is appended to the data in fields
                title, abstract, body, authors = handleUploadedFile(
                    proceedings_form.cleaned_data, request.FILES.get('file'))

                paper = edit(id, title=title,
                    abstract=abstract, body=body,
                    authors=authors) if id else create(title=title,
                    abstract=abstract, body=body,
                    authors=authors)

                # Successfully saved. So get back to the edit page.
                redirect_to = reverse('scipycon_submit_proceedings',
                                      args=[paper.id], kwargs={'scope': scope})
                return set_message_cookie(
                redirect_to, msg = u'Thanks, your paper has been submitted.')
            else:
                # This is impossible. Something was wrong so return back
                # to submit page
                redirect_to = reverse('scipycon_submit_proceedings',
                                      kwargs={'scope': scope})
                return set_message_cookie(
                redirect_to, msg = u'Something is wrong here.')          
    else:
        if id:
            # If id exists initialize the form with old values
            paper = Paper.objects.get(id=id)
            proceedings_form = ProceedingsForm(
                initial={'title': paper.title,
                         'abstract': paper.abstract,
                         'body': paper.body,
                         'authors': ', '.join([
                             author.username for author in paper.authors.all()])
                })
        else:
            # Otherwise create a new form
            proceedings_form = ProceedingsForm()

        register_form = RegisterForm()
        login_form = AuthenticationForm()

    context = RequestContext(request, {
        'proceedings_form': proceedings_form,
        'register_form' : register_form,
        'message' : message,
        'login_form' : login_form
        })

    context['id'] = id if id else None

    return render_to_response(template, context)


def create(**kwargs):
    """View to create a new proceedings.
    """

    title = kwargs.get('title')
    abstract = kwargs.get('abstract')
    body = kwargs.get('body')
    authors = kwargs.get('authors')

    paper = Paper(title=title, abstract=abstract, body=body)
    paper.save()

    if authors:
        authors = authors.split(',')
        for author in authors:
            user = User.objects.get(username=author.strip())
            paper.authors.add(user)

    return paper


def edit(id, **kwargs):
    """View to edit the proceedings paper.
    """

    paper = Paper.objects.get(id=id)

    paper.title = kwargs.get('title')
    paper.abstract = kwargs.get('abstract')
    paper.body = kwargs.get('body')
    authors = kwargs.get('authors')

    if authors:
        authors = authors.split(',')
        for author in authors:
            user = User.objects.get(username=author.strip())
            paper.authors.add(user)

    paper.save()

    return paper


def show_paper(request, id):
    """Display the thumbnail of the rendered paper for download
    """
    
    paper = Paper.objects.get(id=id)

    paper_data = {
      'paper_abstract': paper.abstract,
      'authors': [
          {'first_names': author.first_name,
            'surname': author.last_name,
            'address': 'XXX',
            'country': 'XXX',
            'email_address': 'XXX@xx.com',
            'institution': 'XXX'
           } for author in paper.authors.all()],
      'title': paper.title
      }
    
    abstract = mk_scipy_paper.Bunch(**paper_data)
    abstract.authors = [mk_scipy_paper.Bunch(**a) for a in abstract.authors]

    abstract['paper_text'] = paper.body

    outfilename = '/media/python/workspace/scipycon/project/scipycon/proceedings/booklet/output/paper.pdf'
    attach_dir = os.path.dirname('/media/python/workspace/scipycon/project/scipycon/proceedings/booklet/output/')
    mk_scipy_paper.mk_abstract_preview(abstract, outfilename, attach_dir)

    from django.http import HttpResponse

    # TODO: Return something in the repo
    return HttpResponse('')
