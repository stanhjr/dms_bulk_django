from datetime import timedelta, date, datetime

from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.db.models import Sum
from online_users.models import OnlineUserActivity

from analytics.models import GoogleAnalytics
from analytics.models import UserStatistics
from analytics.tools import get_unique_users_today
from order.models import OrderModel


class GoogleAnalyticsAdmin(ModelAdmin):
    change_list_template = 'admin/google_analytics.html'

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(
            request,
            extra_context=extra_context,
        )
        try:
            users_today = get_unique_users_today()
            today = date.today()
            user_statistics = UserStatistics.objects.filter(created_at=today).first()
            if user_statistics:
                user_statistics.visitors_number = users_today
            else:
                user_statistics = UserStatistics.objects.create(visitors_number=users_today, created_at=today)
            user_statistics.save()

            seven_day_before = today - timedelta(days=7)
            orders_today_sum = OrderModel.objects.filter(created_at__date=today).aggregate(Sum('order_calc__total_integer'))[
                'order_calc__total_integer__sum']
            orders_last_week_sum = \
                OrderModel.objects.filter(created_at__gte=seven_day_before).aggregate(
                    Sum('order_calc__total_integer'))[
                    'order_calc__total_integer__sum']
            orders_all_sum = OrderModel.objects.aggregate(Sum('order_calc__total_integer'))[
                'order_calc__total_integer__sum']

            if not orders_all_sum:
                orders_all_sum = 0
            if not orders_last_week_sum:
                orders_last_week_sum = 0
            if not orders_today_sum:
                orders_today_sum = 0

            users_number_last_week = UserStatistics.objects.filter(created_at__gte=seven_day_before).aggregate(
                Sum('visitors_number'))['visitors_number__sum']
            users_number_all_time = UserStatistics.objects.aggregate(
                Sum('visitors_number'))['visitors_number__sum']
            users_number_today = UserStatistics.objects.filter(created_at=today).aggregate(
                Sum('visitors_number'))['visitors_number__sum']
            if not users_number_last_week:
                users_number_last_week = 0
            if not users_number_all_time:
                users_number_all_time = 0
            if not users_number_today:
                users_number_today = 0

            context = {
                'user_activity_count': OnlineUserActivity.get_user_activities(timedelta(minutes=15)).count(),
                'orders_today_count': OrderModel.objects.filter(created_at__date=today).count(),
                'orders_last_week_count': OrderModel.objects.filter(created_at__gte=seven_day_before).count(),
                'orders_complete_count': OrderModel.objects.count(),
                'orders_today_sum': orders_all_sum,
                'orders_last_week_sum': orders_last_week_sum,
                'orders_all_sum': orders_today_sum,
                'users_number_today': users_number_today,
                'users_number_last_week': users_number_last_week,
                'users_number_all_time': users_number_all_time,
            }

        except (AttributeError, KeyError):
            return response
        response.context_data.update(context)
        return response


admin.site.register(GoogleAnalytics, GoogleAnalyticsAdmin)
