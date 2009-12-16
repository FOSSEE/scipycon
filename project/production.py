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
DATABASE_NAME = 'conference2009'
DATABASE_USER = 'root'
# Imports DATABASE_PASSWORD from project/local.py that is not part of mercurial repo
from project.local import DATABASE_PASSWORD
