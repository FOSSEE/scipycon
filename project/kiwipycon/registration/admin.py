# -*- coding: utf-8 -*-
from __future__ import absolute_import

#django.contrib
from django.contrib import admin

#kiwipycon
from .models import Registration
from .models import Wifi

class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('registrant', 'full_name', 'laptop', 'slug',
            'email', 'city', 'organisation', 'occupation',
            'postcode', 'tshirt', 'conference', 'tutorial',
            'sprint', 'allow_contact')
    fieldsets = (
        ('Details', {
            'fields': ('slug', 'registrant', 'organisation', 'occupation',
                'city', 'tshirt')
        }),
        ('Information', {
            'fields': ('allow_contact',),
        }),
    )

    search_fields = ['registrant__username', 'registrant__email']

    def email(self, obj):
        return obj.registrant.email

    def full_name(self, obj):
        return obj.registrant.get_full_name()

    def laptop(self, obj):
        return obj.registrant.wifi_set.values()[0]['wifi']

admin.site.register(Registration, RegistrationAdmin)

class WifiAdmin(admin.ModelAdmin):
    list_display = ('user', 'wifi',)
    list_filter = ('wifi',)

admin.site.register(Wifi, WifiAdmin)

