import os

from django.conf import settings
from django.template.loader import render_to_string

def save_invoice(user, registration, template_name):
    content = render_to_string(template_name,
        {'registration' : registration, 'user': user})
    filename = '%s.html' % registration.slug
    filepath = os.path.join(settings.USER_MEDIA_PDF, filename)
    save_to_file(content, filepath)

def save_to_pdf(content, filepath):
    import pisa
    pisa.CreatePDF(str(content), file(filepath, 'wb'))

def save_to_file(content, filepath):
    fout = file(filepath, 'wb')
    fout.write(content)
    fout.close()
