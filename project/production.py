#django
from project.settings import *

DEBUG=False
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
    'project.scipycon',
    'project.scipycon.user',
    'project.scipycon.talk',
    'project.scipycon.registration',
    'project.scipycon.proceedings',
    'tagging',
)

DATABASE_ENGINE = 'mysql'
DATABASE_NAME = 'scipycon'
DATABASE_USER = 'scipy'
# Imports DATABASE_PASSWORD from project/local.py that is not part of mercurial repo
from project.local import DATABASE_PASSWORD
