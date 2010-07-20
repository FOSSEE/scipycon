from django.contrib import admin

from project.scipycon.proceedings.models import Paper


class PaperAdmin(admin.ModelAdmin):
    list_display = ('title', 'abstract')
    list_filter = ('title', 'authors')
    search_fields = ('title', 'abstract', 'authors')
    fieldsets = (
        ('Details', {
            'fields': ('title', 'abstract', 'body', 'authors')
        }),
    )

admin.site.register(Paper, PaperAdmin)
