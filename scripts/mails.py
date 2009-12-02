"""Helper script to send emails to the users to remind of the
registration and inform them to complete their profiles and stuff.
"""


__authors__ = [
  '"Madhusudan.C.S" <madhusudancs@gmail.com>',
  ]


from django.template import loader

from project.kiwipycon.talk.models import Talk


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
