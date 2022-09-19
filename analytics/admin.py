from datetime import timedelta

from django.contrib import admin
from django.contrib.admin import ModelAdmin
from online_users.models import OnlineUserActivity

from analytics.models import GoogleAnalytics


class GoogleAnalyticsAdmin(ModelAdmin):
    change_list_template = 'admin/google_analytics.html'

    def changelist_view(self, request, extra_context=None):
        user_activity_count = OnlineUserActivity.get_user_activities(timedelta(minutes=2)).count()

        response = super().changelist_view(
            request,
            extra_context=extra_context,
        )
        try:
            ...
        except (AttributeError, KeyError):
            return response
        response.context_data['content'] = user_activity_count
        return response


admin.site.register(GoogleAnalytics, GoogleAnalyticsAdmin)
