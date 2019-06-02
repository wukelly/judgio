from django.contrib import admin
from django.conf.urls import url
import csv, sys, os

from .models import Judge
from .forms import JudgeForm

# controls /admin/judging/judge
@admin.register(Judge)
class JudgeAdmin(admin.ModelAdmin):
    # override default form
    form = JudgeForm

    # Table columns
    list_display = ('name', 'organization', 'job_title', 'email', 'username', 'sponsor_judge', 'checked_in')
    search_fields = ['user__first_name', 'user__last_name', 'organization', 'user__email']

# new endpoint to add csv import
class JudgeUploadAdmin(admin.AdminSite):
    index_title = 'Judge CSV Upload'

    # change template
    index_template = 'admin/judge_upload.html'

judge_upload_site = JudgeUploadAdmin(name='csv-upload')
