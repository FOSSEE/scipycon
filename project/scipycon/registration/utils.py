from django.core.mail import EmailMessage


def send_confirmation(registrant, event ,password=None):

    message = EmailMessage()
    message.subject = u'Registration to %s' % (event.get_full_name())
    message.from_email = u'admin@scipy.in'
    message.to = [registrant.email]

    details = {'name': registrant.get_full_name(),
               'username': registrant.username,
               'password': password,
               'event_name': event.get_full_name(),
               'event_scope': event.scope,
            }

    confirmation_newuser = """Dear %(name)s,

Thank you, for registering for %(event_name)s!

You may log in to the %(event_name)s website at
http://scipy.in/%(event_scope)s/login using the username -
%(username)s and the password - %(password)s.

Looking forward to meet you at %(event_name)s.

Regards,
SciPy.in Team

If you lose your password, visit: http://scipy.in/password-reset
"""

    message.body = confirmation_newuser %(details)

    message.send()


