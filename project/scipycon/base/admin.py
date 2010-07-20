from django.contrib import admin

from project.scipycon.base.models import Event
from project.scipycon.base.models import Timeline


class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'turn', 'status', 'scope')
    list_filter = ('name', 'turn', 'status',)
    search_fields = ('name', 'turn', 'status',)
    fieldsets = (
        ('Details', {
            'fields': ('name', 'turn', 'status', 'scope')
        }),
    )


class TimelineAdmin(admin.ModelAdmin):
    list_display = ('registration_start', 'registration_end', 'cfp_start',
                    'cfp_end', 'accepted_papers_announced',
                    'proceedings_paper_deadline', 'event_start',
                    'event_end', 'event')
    list_filter = ('registration_start', 'registration_end', 'cfp_start',
                   'cfp_end', 'accepted_papers_announced',
                   'proceedings_paper_deadline', 'event_start',
                   'event_end', 'event')
    search_fields = ('registration_start', 'registration_end', 'cfp_start',
                     'cfp_end', 'accepted_papers_announced',
                     'proceedings_paper_deadline', 'event_start',
                     'event_end')
    fieldsets = (
        ('Registration', {
            'fields': ('registration_start', 'registration_end')
        }),
        ('Call for Papers', {
            'fields': ('cfp_start', 'cfp_end', 'accepted_papers_announced',
                       'proceedings_paper_deadline')
        }),
        ('Event', {
            'fields': ('event_start', 'event_end', 'event')
        }),
    )

admin.site.register(Event, EventAdmin)
admin.site.register(Timeline, TimelineAdmin)
