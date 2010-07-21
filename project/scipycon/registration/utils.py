from django.core.mail import EmailMessage


def send_confirmation(registrant, event):

    message = EmailMessage()
    message.subject = u'Registration to %s' % (event.get_full_name())
    message.from_email = u'admin@scipy.in'
    message.to = [registrant.email]

    username = registrant.username
    all = {'name': registrant.get_full_name(),
           'username': username,
           'event_name': event.get_full_name(),
           'event_scope': event.scope,
           }

    message.send()

confirmation_newuser = """Dear %(name)s,

Welcome to %(event_name)s. You have registered for %(event_name)s with the
username %(username)s. You may log in to the %(event_name)s website at
http://scipy.in/%(event_scope)s/login using the given username

Thank you for your registration! Looking forward to meet you at %(event_name)s.

Regards,
The SciPy.in Team

If you lose your password to the website please visit:
http://scipy.in/password-reset
"""
