# -*- coding: utf-8 -*-
from __future__ import absolute_import

# django
from django.core.mail import EmailMessage

def send_confirmation(registrant, invoice, password=None, sponsor=None,
        amount=None):

    message = EmailMessage()
    message.subject = u'Registration to SciPy.in 2009'
    message.from_email = u'admin@scipy.in'
    message.to = [registrant.email]
    name = '%s %s' % (registrant.first_name, registrant.last_name)
    if name.strip() == '':
        name = registrant.username

    username = registrant.username
    all = {'name': name,
            'password': password,
            'username': username}

    if password:
        message.body = confirmation_newuser % all
    else:
        message.body = confirmation_currentuser % all

    message.send()

def send_confirmation_payment_email(registrant):
    message = EmailMessage()
    message.subject = u'Registration payment to SciPy.in 2009'
    message.from_email = u'admin@scipy.in'
    message.to = [registrant.email]
    name = '%s %s' % (registrant.first_name, registrant.last_name)
    username = registrant.username
    if name.strip() == '':
        name = registrant.username
    message.body = confirmation_payment % dict(name=name,
            username=username)
    message.send()

def send_banking_fix_email(registrant, invoicenum):
    message = EmailMessage()
    message.subject = u'Registration invoice update to SciPy.in 2009'
    message.from_email = u'admin@scipy.in'
    message.to = [registrant.email]
    name = '%s %s' % (registrant.first_name, registrant.last_name)
    username = registrant.username
    if name.strip() == '':
        name = registrant.username
    message.body = banking_fix % dict(name=name,
            username=username, invoice=invoicenum)
    message.send()

banking_fix = """
Dear %(name)s,

Invoice update to Kiwi Pycon 2009.

Ooops. We made the invoice number too long to be entered for internet banking.
We have therefore changed the prefix and your new invoice number is:
%(invoice)s

You will find that your online invoice has been updated. Thanks for your
patience.

http://nz.pycon.org/invoice
A pdf version here:
http://nz.pycon.org/pdf_invoice

Regards,
The Kiwi Pycon 2009 Team

Your username, in case you've forgotten: %(username)s.

If you have lost your password to the website please visit:
http://nz.pycon.org/password-reset

    """

confirmation_payment = """
Dear %(name)s,

Welcome to Kiwi Pycon 2009.

Your payment has been received and your attendence confirmed.

Many thanks!

You can view your invoice at:
http://nz.pycon.org/invoice
And a pdf version here:
http://nz.pycon.org/pdf_invoice

Regards,
The Kiwi Pycon 2009 Team

Your username, in case you've forgotten: %(username)s.

If you have lost your password to the website please visit:
http://nz.pycon.org/password-reset

    """

confirmation_newuser = """
Dear %(name)s,

Welcome to SciPy.in 2009. You may log in to 
http://scipy.in/login using the following credentials:

Username: %(username)s
Password: %(password)s

There is an entry fee for the SciPy conference only. However
the sprint and tutorials don't have any entry fee. The entry
fee for the conference can be paid on the spot on the first
day of the conference.

Thanks for your registration!

Regards,
The SciPy.in Team

If you lose your password to the website please visit:
http://scipy.in/password-reset
    """

confirmation_sponsoreduser = """
Dear %(name)s,

Welcome to Kiwi Pycon 2009.

Your username is: %(username)s

Your registration has been accepted as a guest of %(stype)s 
sponsor %(sname)s.

Thanks!

Regards,
The Kiwi Pycon 2009 Team

If you have lost your password to the website please visit:
http://nz.pycon.org/password-reset

    """

confirmation_sponsorednewuser = """
Dear %(name)s,

Welcome to Kiwi Pycon 2009.

Your username is: %(username)s
Your password is: %(password)s

Your registration has been accepted as a guest of %(stype)s sponsor %(sname)s.

Thanks!

Regards,
The Kiwi Pycon 2009 Team

If you lose your password to the website please visit:
http://nz.pycon.org/password-reset

    """

confirmation_currentuser = """
Dear %(name)s,

Welcome to SciPy.in 2009. You may log in to 
http://scipy.in/login using the following credentials:

Username: %(username)s
Password: %(password)s

There is an entry fee for the SciPy conference only. However
the sprint and tutorials don't have any entry fee. The entry
fee for the conference can be paid on the spot on the first
day of the conference. 

Thanks for your registration!

Regards,
The SciPy.in Team

If you lose your password to the website please visit:
http://scipy.in/password-reset
    """
