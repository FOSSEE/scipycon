#django
from django.conf.urls.defaults import include
from django.conf.urls.defaults import patterns
from django.conf import settings
from django.contrib import admin
from django.views.generic.simple import direct_to_template
from django.conf.urls.defaults import *

#basic.blog
from basic.blog.feeds import BlogPostsFeed

feeds = {
    'blog': BlogPostsFeed,
    }

admin.autodiscover()

# Blog & Admin
urlpatterns = patterns(
    '',
    url(r'^$', 
        direct_to_template, {"template": "home.html"},
        name='home'),
    (r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}),
    (r'^comments/', include('django.contrib.comments.urls')),
    (r'^admin/(.*)', admin.site.root),
)

# Talks, etc.
urlpatterns += patterns('project.kiwipycon.talk.views',
    url(r'^talks/$',  'list_talks', name='list_talks'),
    url(r'^talks/talk/(?P<id>\d+)/$',  'talk', name='talk_detail'),
    url(r'^submit-talk/$',  'submit_talk', name='kiwipycon_submit_talk'),
    url(r'^edit-talk/(?P<id>\d+)/$',  'edit_talk', name='kiwipycon_edit_talk'),
    )

# Registration
urlpatterns += patterns('project.kiwipycon.registration.views',
    url(r'^invoice/$',  'invoice', name='kiwipycon_invoice'),
    url(r'^pdf_invoice/$',  'pdf_invoice', name='kiwipycon_pdf_invoice'),
    url(r'^registrations/$',  'registrations', name='kiwipycon_registrations'),
    url(r'^submit-registration/$',  'submit_registration', name='kiwipycon_submit_registration'),
    url(r'^edit-registration/(?P<id>\d+)/$',  'edit_registration',
        name='kiwipycon_edit_registration'),
    url(r'^download_csv/', 'download_csv', name="download_csv"),
    )


# Authentication and Profile
urlpatterns += patterns('project.kiwipycon.user.views',
    url(r'^login/$',  'login', name='kiwipycon_login'),
    url(r'^logout/$',  'logout', name='kiwipycon_logout'),
    url(r'^account/$',  'account', name='kiwipycon_account'),
    url(r'^password/$', 'password', name='kiwipycon_password'), # change pwd
    url(r'^username/$', 'username', name='kiwipycon_username'), # change uname
    url(r'^edit-profile/$', 'edit_profile', name='kiwipycon_edit_profile'),
    )

# About pages and all other static html pages
urlpatterns += patterns('',
    url(r'^about/accommodation/$', 
        direct_to_template, {"template": "about/accommodation.html"},
        name='accommodation'),
    url(r'^about/food/$',
        direct_to_template, {"template": "about/food.html"}, name='food'),
    url(r'^about/venue/$',
        direct_to_template, {"template": "about/venue.html"}, name='venue'),
    url(r'^about/reaching/$', 
        direct_to_template, {"template": "about/reaching.html"},
        name='reaching'),
    url(r'^talks-cfp/$', 
        direct_to_template, {"template": "talk/talks-cfp.html"},
        name='talks-cfp'),
    url(r'^talks-cfp/schedule/$', 
        direct_to_template, {"template": "talk/schedule.html"},
        name='schedule'),
    url(r'^talks-cfp/speakers/$', 
        direct_to_template, {"template": "talk/speakers.html"},
        name='speakers'),
    (r'^accounts/', include('registration.urls')),
    )

# Password reset
urlpatterns += patterns('django.contrib.auth.views',
     url(r'^password-reset/$', 'password_reset', name='kiwipycon_password_reset'),
     url(r'^password-reset-done/$', 'password_reset_done'),
     url(r'^password-reset-confirm/(?P<uidb36>[-\w]*)/(?P<token>[-\w]*)$', 'password_reset_confirm'),
     url(r'^password-reset-complete/$', 'password_reset_complete'),
)

# Serve static files in DEBUG = True mode
if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': settings.MEDIA_ROOT}),
        (r'^(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': settings.STATIC_ROOT}),
    )
