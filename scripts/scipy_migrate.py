"""Helper script to send an email to all users who registered
before activation logic was implemented. This script can be 
run only within a Django shell.
"""


__authors__ = [
  '"Madhusudan.C.S" <madhusudancs@gmail.com>',
  ]


from datetime import datetime

from django.template import loader

from registration.models import RegistrationProfile


def remind_users():
    regs = RegistrationProfile.objects.filter(
        user__is_active=0,
        user__date_joined__lte=datetime(2009, 10, 13))

    template = 'notifications/activate_mail.html'

    for reg in regs:

        subject = 'Update and activate your SciPy.in registration.'
        message = loader.render_to_string(
            template, dictionary={'activation_key': reg.activation_key,
                                  'name': reg.user.username})

        reg.user.email_user(subject=subject, message=message,
                            from_email='admin@scipy.in')
