from django.contrib import admin
import csv, sys, os

from .models import Judge

# controls /admin/judging/display
class JudgeAdmin(admin.ModelAdmin):
    # editing judge form fields
    fieldsets = [
        ('General Information',     {'fields': ['first_name',
                                                'last_name',
                                                'organization',
                                                'job_title',
                                                'sponsor_judge']}),
        ('Event Day',               {'fields': ['checked_in']}),
    ]

    # Table columns
    list_display = ('name', 'organization', 'job_title', 'email', 'sponsor_judge', 'checked_in')
    search_fields = ['user__first_name', 'user__last_name', 'organization', 'user__email']

# add import from csv option


admin.site.register(Judge, JudgeAdmin)
