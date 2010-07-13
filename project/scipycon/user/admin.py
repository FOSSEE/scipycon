# -*- coding: utf-8 -*-
from __future__ import absolute_import

#django
from django.contrib import admin

#scipycon
from .models import UserProfile

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'email',  'url', 'about')

    def email(self, obj):
        return obj.user.email

admin.site.register(UserProfile, UserProfileAdmin)

