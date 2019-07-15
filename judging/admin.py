from django.contrib import admin, messages
from django.contrib.auth.models import User

from .models import Judge
from .forms import JudgeForm
from .views import judge_upload_view

# Filter for active status
class ActiveFilter(admin.SimpleListFilter):
    title = 'Active'
    parameter_name = 'active'

    def lookups(self, request, model_admin):
        return [
            ('active', 'Active'),
            ('not_active', 'Not Active'),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'active':
            return queryset.distinct().filter(active=True)
        if self.value():
            return queryset.distinct().filter(active=False)


# controls /admin/judging/judge
class JudgeAdmin(admin.ModelAdmin):
    # override default form
    form = JudgeForm

    # Table columns on form
    list_display = ('name', 'organization', 'job_title', 'email', 'username', 'sponsor_judge', 'checked_in', 'active')
    search_fields = ['user__first_name', 'user__last_name', 'organization', 'user__email']
    list_filter = (ActiveFilter, )

# register new view on admin site
admin.site.register(User)
admin.site.register(Judge, JudgeAdmin)
admin.site.register_view('judge/judge-upload/', view=judge_upload_view)
