#django
from project.settings import *

DEBUG=True
TEMPLATE_DEBUG=DEBUG

SITE_ID = 2

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.comments',
    'django.contrib.sessions',
    'django.contrib.admin',
    'django.contrib.sites',
    'django.contrib.flatpages',
    'django.contrib.markup',
    'django.contrib.sitemaps',
    'project.scipycon',
    'project.scipycon.base',
    'project.scipycon.proceedings',
    'project.scipycon.registration',
    'project.scipycon.user',
    'project.scipycon.talk',
    'tagging',
    'robots',
    'south',
)

DATABASE_ENGINE = 'sqlite3'
DATABASE_NAME = 'scipycon.db'
DATABASE_USER = ''
DATABASE_PASSWORD = ''

EMAIL_HOST = 'localhost'
EMAIL_PORT = '1025'
# print to standard output:
# python -m smtpd -n -c DebuggingServer localhost:1025
