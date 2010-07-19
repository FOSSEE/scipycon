
import os

ADMINS = (
    ('Madhusudan.C.S', 'admin@scipy.in'),
)

MANAGERS = ADMINS

DATABASE_HOST = ''
DATABASE_PORT = ''

TIME_ZONE = 'Asia/Kolkata'

LANGUAGE_CODE = 'en-us'

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(os.path.dirname(__file__), 'media')

USER_MEDIA_ROOT = os.path.join(os.path.dirname(__file__), 'media', 'user')
USER_MEDIA_PDF = os.path.join(os.path.dirname(__file__), 'media', 'pdf')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'

USER_MEDIA_URL = '/media/user/'

# Absolute path to the directory that holds static files.
# Example: "/home/static-files/static-files.lawrence.com/"
STATIC_ROOT = os.path.join(os.path.dirname(__file__), 'static')

# URL that handles the static files served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://static-files.lawrence.com", "http://example.com/static-files/"
STATIC_URL = '/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/admin_media/'

# Don't share this with anybody.
SECRET_KEY = 'o)l1m*xi4%7*2dkbwcou2vc48vo8v48y3obyou3hb3bh$t25zd'

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.doc.XViewMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
)

ROOT_URLCONF = 'project.urls'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
)

TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(__file__), "templates"),
)

LOGIN_URL = "/login"

AUTH_PROFILE_MODULE = 'user.UserProfile'

TEMPLATE_CONTEXT_PROCESSORS = (
        'django.core.context_processors.auth',
        'django.core.context_processors.debug',
        'django.core.context_processors.i18n',
        'django.core.context_processors.media')

DEFAULT_FROM_EMAIL = 'admin@scipy.in'

CURRENT_SCOPE = 'scipyin/2010'
