from django.contrib import admin
from django.contrib.admin import ModelAdmin

from analytics.models import GoogleAnalytics


class GoogleAnalyticsAdmin(ModelAdmin):
    change_list_template = 'admin/google_analytics.html'

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(
            request,
            extra_context=extra_context,
        )
        try:
            ...
        except (AttributeError, KeyError):
            return response
        response.context_data['content'] = 'Какой то контент'
        return response


admin.site.register(GoogleAnalytics, GoogleAnalyticsAdmin)