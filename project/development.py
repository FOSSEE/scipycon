#django
from project.settings import *

DEBUG=True
TEMPLATE_DEBUG=DEBUG

SITE_ID = 1

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.comments',
    'django.contrib.sessions',
    'django.contrib.admin',
    'django.contrib.sites',
    'django.contrib.flatpages',
    'django.contrib.markup',
    'project.kiwipycon',
    'project.kiwipycon.user',
    'project.kiwipycon.talk',
    'project.kiwipycon.registration',
    'project.kiwipycon.sponsor',
    'tagging',
    'basic.blog',
    'basic.inlines',
    'basic.media',
    'django_extensions',
    'south',
    'registration',
)

DATABASE_ENGINE = 'mysql'
DATABASE_NAME = 'conference'
DATABASE_USER = 'root'
DATABASE_PASSWORD = ''

EMAIL_HOST = 'localhost'
EMAIL_PORT = '1025'
# print to standard output:
# python -m smtpd -n -c DebuggingServer localhost:1025

