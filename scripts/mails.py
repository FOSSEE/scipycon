"""Helper script to send emails to the users to remind of the
registration and inform them to complete their profiles and stuff.
"""


__authors__ = [
  '"Madhusudan.C.S" <madhusudancs@gmail.com>',
  ]


from django.template import loader
from django.contrib.auth.models import User

from project.scipycon.registration.models import Registration
from project.scipycon.talk.models import Talk


def speaker_accepted():
    """Sends a mail to each speaker whose talk has been accepted
    informing them about the same.
    """

    talks = Talk.objects.all()

    template = 'notifications/speaker_accepted_mail.html'

    for talk in talks:
        subject = 'Your talk has been selected for SciPy.in 2009!'
        message = loader.render_to_string(
            template, dictionary={'name': talk.speaker.username,
                                  'title': talk.title})

        talk.speaker.email_user(subject=subject, message=message,
                                from_email='admin@scipy.in')


def speaker_sponsorship():
    """Sends a mail to each speaker whose talk has been accepted
    informing them about the their sponsorship.
    """

    talks = Talk.objects.all()

    template = 'notifications/speaker_sponsorship_mail.html'

    for talk in talks:
        subject = 'Details regarding your travel and accommodation for SciPy.in 2009'
        message = loader.render_to_string(
            template, dictionary={'name': talk.speaker.username,
                                  'title': talk.title})

        talk.speaker.email_user(subject=subject, message=message,
                                from_email='admin@scipy.in')


def delegate_remainder(template=None):
    """Sends a mail to each delegate about the template content specified.
    """

    regs = Registration.objects.all()

    for reg in regs:
        subject = 'SciPy.in 2010: Registration updates required for confirmation'
        message = loader.render_to_string(
            template, dictionary={'name': reg.registrant.get_full_name()})

        reg.registrant.email_user(subject=subject, message=message,
                                  from_email='info@scipy.in')


def delegate_about_event():
    """Sends a mail to each confirmed delegate informing
    them about the the individual events.
    """

    regs = Registration.objects.all()

    template = 'notifications/sprints_about_mail.html'

    for reg in regs:
        subject = 'SciPy.in 2009: Details of the individual events'
        message = loader.render_to_string(
            template, dictionary={'name': reg.registrant.username})

        reg.registrant.email_user(subject=subject, message=message,
                                  from_email='madhusudancs@gmail.com')


def delegate_last_day():
    """Sends a mail to each confirmed delegate informing
    them about the final details.
    """

    regs = Registration.objects.all()

    template = 'notifications/last_day_mail.html'

    for reg in regs:
        subject = 'SciPy.in 2009: Schedule and other details'
        message = loader.render_to_string(
            template, dictionary={'name': reg.registrant.username})

        reg.registrant.email_user(subject=subject, message=message,
                                  from_email='madhusudancs@gmail.com')


def speaker_confirmation():
    """Sends a mail to each speaker asking for confirmation.
    """

    talks = Talk.objects.all()

    template = 'notifications/speaker_confirmation_mail.html'

    for talk in talks:
        subject = 'SciPy.in 2009: Requesting for confirmation of your talk'
        message = loader.render_to_string(
            template, dictionary={'name': talk.speaker.username,
                                  'title': talk.title})

        talk.speaker.email_user(subject=subject, message=message,
                                from_email='admin@scipy.in')

def proceedings_detail():
    """Sends a mail to each speaker informing them about proceedings
    """

    talks = Talk.objects.all()

    template = 'notifications/proceedings_detail_mail.html'

    for talk in talks:
        subject = 'SciPy.in 2009 Proceedings'
        message = loader.render_to_string(
            template, dictionary={'name': talk.speaker.username})

        talk.speaker.email_user(subject=subject, message=message,
                                from_email='admin@scipy.in')
