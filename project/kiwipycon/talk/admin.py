# -*- coding: utf-8 -*-
from __future__ import absolute_import

#django.contrib
from django.contrib import admin

#kiwipycon
from .models import Talk

class TalkAdmin(admin.ModelAdmin):
    list_display = ('title', 'speaker', 'topic', 'duration', 'audience', 'approved')
    list_filter = ('approved', 'audience', 'topic', 'speaker')
    search_fields = ('slug', 'title', 'abstract')
    prepopulate_from = {'slug': ('title',)}
    fieldsets = (
        ('Details', {
            'fields': ('slug', 'title', 'abstract', 'speaker')
        }),
        ('Information', {
            'fields': ('topic', 'duration', 'audience', 'approved')
        }),
    )
admin.site.register(Talk, TalkAdmin)
