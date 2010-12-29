from django.conf import settings
from django.conf.urls.defaults import include
from django.conf.urls.defaults import patterns
from django.conf.urls.defaults import url
from django.contrib import admin
from django.views.generic.simple import direct_to_template
from django.views.generic.simple import redirect_to


admin.autodiscover()

PROGRAM_PATTERN_CORE = r'[a-z](?:[0-9a-z]|_[0-9a-z])*'
EVENT_PATTERN_CORE =r'(?:[0-9a-z]|_[0-9a-z])*' 
SCOPE_ARG_PATTERN = r'(?P<scope>%s/%s)' % (
    PROGRAM_PATTERN_CORE, EVENT_PATTERN_CORE) 

sitemaps = {}

# Admin
urlpatterns = patterns('',
    (r'^admin/(.*)', admin.site.root),
    (r'^comments/', include('django.contrib.comments.urls')),
    (r'^robots\.txt$', include('robots.urls')),
    (r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
    url(r'^$', redirect_to, {'url': '/%s/' % (settings.CURRENT_SCOPE)}),
    url(r'^%s/$' % (SCOPE_ARG_PATTERN),
        direct_to_template, {"template": "home.html"}, name='home'),
)

# Talks, etc.
urlpatterns += patterns('project.scipycon.talk.views',
    url(r'^%s/talks/$' % (SCOPE_ARG_PATTERN),
        'list_talks', name='list_talks'),
    url(r'^%s/my-talks/$' % (SCOPE_ARG_PATTERN),
        'list_my_talks', name='list_my_talks'),
    url(r'^%s/talks/talk/(?P<id>\d+)/$' % (SCOPE_ARG_PATTERN),
        'talk', name='talk_detail'),
    url(r'^%s/submit-talk/$' % (SCOPE_ARG_PATTERN),
        'submit_talk', name='scipycon_submit_talk'),
    url(r'^%s/edit-talk/(?P<id>\d+)/$' % (SCOPE_ARG_PATTERN),
        'edit_talk', name='scipycon_edit_talk'),
    url(r'^%s/list-talks/(?P<id>\d+)/$' % (SCOPE_ARG_PATTERN),
        'list_talks', name='scipycon_list_talk'),
    url(r'^%s/download_slides/$' % (SCOPE_ARG_PATTERN),
        'download_slides', name='scipycon_download_slides'),
    url(r'^%s/download_videos/$' % (SCOPE_ARG_PATTERN),
        'download_videos', name='scipycon_download_videos'),

    )

# Registration
urlpatterns += patterns('project.scipycon.registration.views',
    url(r'^%s/registrations/$' % (SCOPE_ARG_PATTERN), 'registrations',
        name='scipycon_registrations'),
    url(r'^%s/submit-registration/$' % (SCOPE_ARG_PATTERN),
        'submit_registration', name='scipycon_submit_registration'),
    url(r'^%s/edit-registration/(?P<id>\d+)/$' % (SCOPE_ARG_PATTERN),
        'edit_registration', name='scipycon_edit_registration'),
    url(r'^%s/regstats/$'% (SCOPE_ARG_PATTERN),
        'regstats', name="scipycon_regstats"),
    url(r'^%s/regstats/download$'% (SCOPE_ARG_PATTERN),
        'regstats_download', name="scipycon_regstats_download"),
    url(r'^%s/manage_payments/$'% (SCOPE_ARG_PATTERN),
        'manage_payments', name="scipycon_manage_payments"),
    )

# Authentication and Profile
urlpatterns += patterns('project.scipycon.user.views',
    url(r'^%s/login/$' % (SCOPE_ARG_PATTERN),
        'login', name='scipycon_login'),
    url(r'^%s/logout/$' % (SCOPE_ARG_PATTERN),
        'logout', name='scipycon_logout'),
    url(r'^%s/account/$' % (SCOPE_ARG_PATTERN),
        'account', name='scipycon_account'),
    url(r'^%s/password/$' % (SCOPE_ARG_PATTERN),
        'password', name='scipycon_password'), # change pwd
    url(r'^%s/username/$' % (SCOPE_ARG_PATTERN),
        'username', name='scipycon_username'), # change uname
    url(r'^%s/edit-profile/$' % (SCOPE_ARG_PATTERN),
        'edit_profile', name='scipycon_edit_profile'),
    url(r'^%s/get-usernames/$' % (SCOPE_ARG_PATTERN),
        'get_usernames', name='scipycon_get_usernames'),
    url(r'^%s/get-user-dump/$' % (SCOPE_ARG_PATTERN),
        'get_user_dump', name='scipycon_get_usernames'),
    url(r'^%s/badge/$' % (SCOPE_ARG_PATTERN),
        'badge', name='scipycon_badge'))
    

# Proceedings
urlpatterns += patterns('project.scipycon.proceedings.views',
    url(r'^%s/proceedings/submit/$' % (SCOPE_ARG_PATTERN), 'submit',
        name='scipycon_submit_proceedings'),
    url(r'^%s/proceedings/submit/(?P<id>\d+)/$' % (SCOPE_ARG_PATTERN),
        'submit', name='scipycon_submit_proceedings'),
    url(r'^%s/proceedings/show_paper/(?P<id>\d+)/$' % (SCOPE_ARG_PATTERN),
        'show_paper', name='scipycon_show_paper'),
    )

# About pages and all other static html pages
urlpatterns += patterns('',
    url(r'^%s/about/accommodation/$' % (SCOPE_ARG_PATTERN),
        direct_to_template, {"template": "about/accommodation.html"},
        name='scipycon_accommodation'),
    url(r'^%s/about/food/$' % (SCOPE_ARG_PATTERN),
        direct_to_template, {"template": "about/food.html"},
        name='scipycon_food'),
    url(r'^%s/about/venue/$' % (SCOPE_ARG_PATTERN),
        direct_to_template, {"template": "about/venue.html"},
        name='scipycon_venue'),
    url(r'^%s/about/reaching/$' % (SCOPE_ARG_PATTERN),
        direct_to_template, {"template": "about/reaching.html"},
        name='scipycon_reaching'),
    url(r'^%s/about/city/$' % (SCOPE_ARG_PATTERN),
        direct_to_template, {"template": "about/city.html"},
        name='scipycon_city'),
    url(r'^%s/talks-cfp/$' % (SCOPE_ARG_PATTERN),
        direct_to_template, {"template": "talk/talks-cfp.html"},
        name='scipycon_talks_cfp'),
    url(r'^%s/talks-cfp/schedule/$' % (SCOPE_ARG_PATTERN),
        direct_to_template, {"template": "talk/schedule.html"},
        name='scipycon_schedule'),
    # url(r'^%s/talks-cfp/tutorial/$' % (SCOPE_ARG_PATTERN),
    #     direct_to_template, {"template": "talk/tutorial-schedule.html"},
    #     name='scipycon_tutorial_schedule'),
    # url(r'^%s/talks-cfp/sprint/$' % (SCOPE_ARG_PATTERN),
    #     direct_to_template, {"template": "talk/sprint-schedule.html"},
    #     name='scipycon_sprint_schedule'),
    url(r'^%s/talks-cfp/speakers/$' % (SCOPE_ARG_PATTERN),
        direct_to_template, {"template": "talk/speakers.html"},
        name='scipycon_speakers'),
    url(r'^%s/publicity/$' % (SCOPE_ARG_PATTERN),
        direct_to_template, {"template": "about/publicity.html"},
        name='scipycon_publicity'),
    url(r'^%s/about/fees/$' % (SCOPE_ARG_PATTERN),
        direct_to_template, {"template": "about/fees.html"},
        name='scipycon_fees'),
    url(r'^%s/organizers/$' % (SCOPE_ARG_PATTERN),
        direct_to_template, {"template": "about/organizers.html"},
        name='scipycon_organizers'),
    url(r'^%s/talks-cfp/conference/$' % (SCOPE_ARG_PATTERN),
        direct_to_template, {"template": "talk/conf_schedule.html"},
        name='scipycon_conference'),
    url(r'^%s/tutorial/$' % (SCOPE_ARG_PATTERN),
        direct_to_template, {"template": "about/tutorial.html"},
        name='scipycon_tutorial'),
    url(r'^%s/sprints/$' % (SCOPE_ARG_PATTERN),
        direct_to_template, {"template": "about/sprints.html"},
        name='scipycon_sprints'),
    url(r'^%s/certificates/$' % (SCOPE_ARG_PATTERN),
        direct_to_template, {"template": "about/certificates.html"},
        name='scipycon_certificates'),
    url(r'^%s/about/dates/$' % (SCOPE_ARG_PATTERN),
        direct_to_template, {"template": "about/important_dates.html"},
        name='scipycon_imp_dates'),
    url(r'^%s/about/sponsors/$' % (SCOPE_ARG_PATTERN),
        direct_to_template, {"template": "about/sponsors.html"},
        name='scipycon_sponsors'),
    )

# Password reset
urlpatterns += patterns('django.contrib.auth.views',
     url(r'^password-reset/$', 'password_reset', name='scipycon_password_reset'),
     url(r'^password-reset-done/$', 'password_reset_done'),
     url(r'^password-reset-confirm/(?P<uidb36>[-\w]*)/(?P<token>[-\w]*)$', 'password_reset_confirm'),
     url(r'^password-reset-complete/$', 'password_reset_complete'),
)

handler404 = 'django.views.defaults.page_not_found'

# Serve static files in DEBUG = True mode
if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': settings.MEDIA_ROOT}),
        (r'^static/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': settings.STATIC_ROOT}),
    )
