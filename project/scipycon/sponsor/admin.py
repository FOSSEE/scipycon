# -*- coding: utf-8 -*-
from __future__ import absolute_import

#django
from django.contrib import admin

#kiwipycon
from .models import Sponsor

class SponsorAdmin(admin.ModelAdmin):
    list_display = ('title', 'type', 'contact_name', 'contact_email', 'contact_phone',
            'guests', 'url', 'logo')

admin.site.register(Sponsor, SponsorAdmin)

