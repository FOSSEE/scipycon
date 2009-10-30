#django
from project.settings import *

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
)

DATABASE_ENGINE = 'postgresql_psycopg2'
DATABASE_NAME = 'kpc09'
DATABASE_USER = 'kpc09'
# Imports DATABASE_PASSWORD from project/local.py that is not part of mercurial repo
from project.local import DATABASE_PASSWORD
