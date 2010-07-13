#django
from django.conf.urls.defaults import include
from django.conf.urls.defaults import patterns
from django.conf import settings
from django.contrib import admin
from django.views.generic.simple import direct_to_template
from django.conf.urls.defaults import *

admin.autodiscover()

# Admin
urlpatterns = patterns('',
    url(r'^$',  direct_to_template, {"template": "home.html"}, name='home'),
    (r'^comments/', include('django.contrib.comments.urls')),
    (r'^admin/(.*)', admin.site.root),
)

# Talks, etc.
urlpatterns += patterns('project.scipycon.talk.views',
    url(r'^talks/$', 'list_talks', name='list_talks'),
    url(r'^talks/talk/(?P<id>\d+)/$', 'talk', name='talk_detail'),
    url(r'^submit-talk/$', 'submit_talk', name='scipycon_submit_talk'),
    url(r'^edit-talk/(?P<id>\d+)/$', 'edit_talk', name='scipycon_edit_talk'),
    url(r'^talks-cfp/list-talks/(?P<id>\d+)/$', 'list_talks',
        name='scipycon_list_talk'),
    )

# Registration
urlpatterns += patterns('project.scipycon.registration.views',
    url(r'^registrations/$', 'registrations', name='scipycon_registrations'),
    url(r'^submit-registration/$', 'submit_registration', name='scipycon_submit_registration'),
    url(r'^edit-registration/(?P<id>\d+)/$', 'edit_registration',
        name='scipycon_edit_registration'),
    url(r'^download_csv/', 'download_csv', name="download_csv"),
    )


# Authentication and Profile
urlpatterns += patterns('project.scipycon.user.views',
    url(r'^login/$', 'login', name='scipycon_login'),
    url(r'^logout/$', 'logout', name='scipycon_logout'),
    url(r'^account/$', 'account', name='scipycon_account'),
    url(r'^password/$', 'password', name='scipycon_password'), # change pwd
    url(r'^username/$', 'username', name='scipycon_username'), # change uname
    url(r'^edit-profile/$', 'edit_profile', name='scipycon_edit_profile'),
    url(r'^get-usernames/$', 'get_usernames', name='scipycon_get_usernames'),
    )

# Proceedings
urlpatterns += patterns('project.scipycon.proceedings.views',
    url(r'^proceedings/submit/$', 'submit',
        name='scipycon_submit_proceedings'),
    url(r'^proceedings/submit/(?P<id>\d+)/$', 'submit', 
        name='scipycon_submit_proceedings'),
    url(r'^proceedings/show_paper/(?P<id>\d+)/$', 'show_paper', 
        name='scipycon_show_paper'),
    )

# About pages and all other static html pages
urlpatterns += patterns('',
    url(r'^about/accommodation/$', 
        direct_to_template, {"template": "about/accommodation.html"},
        name='scipycon_accommodation'),
    url(r'^about/food/$',
        direct_to_template, {"template": "about/food.html"}, name='scipycon_food'),
    url(r'^about/venue/$',
        direct_to_template, {"template": "about/venue.html"}, name='scipycon_venue'),
    url(r'^about/reaching/$', 
        direct_to_template, {"template": "about/reaching.html"},
        name='scipycon_reaching'),
    url(r'^talks-cfp/$', 
        direct_to_template, {"template": "talk/talks-cfp.html"},
        name='scipycon_talks_cfp'),
    url(r'^talks-cfp/schedule/$', 
        direct_to_template, {"template": "talk/schedule.html"},
        name='scipycon_schedule'),
    url(r'^talks-cfp/tutorial/$', 
        direct_to_template, {"template": "talk/tutorial-schedule.html"},
        name='scipycon_tutorial_schedule'),
    url(r'^talks-cfp/sprint/$', 
        direct_to_template, {"template": "talk/sprint-schedule.html"},
        name='scipycon_sprint_schedule'),
    url(r'^talks-cfp/speakers/$', 
        direct_to_template, {"template": "talk/speakers.html"},
        name='scipycon_speakers'),
    )

# Password reset
urlpatterns += patterns('django.contrib.auth.views',
     url(r'^password-reset/$', 'password_reset', name='scipycon_password_reset'),
     url(r'^password-reset-done/$', 'password_reset_done'),
     url(r'^password-reset-confirm/(?P<uidb36>[-\w]*)/(?P<token>[-\w]*)$', 'password_reset_confirm'),
     url(r'^password-reset-complete/$', 'password_reset_complete'),
)

# Serve static files in DEBUG = True mode
if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': settings.MEDIA_ROOT}),
        (r'^static/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': settings.STATIC_ROOT}),
    )
