# -*- coding: utf-8 -*-
from __future__ import absolute_import

#django.contrib
from django.contrib import admin

#scipycon
from .models import Accommodation
from .models import Payment
from .models import Registration
from .models import Wifi

class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('registrant', 'full_name', 'phone_num', 
                    'laptop', 'slug', 'email', 'city',
                    'organisation', 'occupation', 'postcode',
                    'tshirt', 'conference', 'tutorial',
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

class AccommodationAdmin(admin.ModelAdmin):
    list_display = ('user', 'sex', 'accommodation_required',
                    'accommodation_days')

admin.site.register(Accommodation, AccommodationAdmin)

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'confirmed', 'acco_confirmed')

admin.site.register(Payment, PaymentAdmin)


