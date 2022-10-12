from datetime import date

from django.utils.deprecation import MiddlewareMixin

from analytics.models import UserStatistics


class VisitCounterMiddleware(MiddlewareMixin):
    def process_request(self, request):
        num_visits = request.session.get('num_visits')
        if not num_visits:
            user_statistics = UserStatistics.objects.filter(created_at=date.today()).first()
            if user_statistics:
                user_statistics.visitors_number += 1
                user_statistics.save()
            else:
                UserStatistics.objects.create(visitors_number=1, created_at=date.today())
            request.session['num_visits'] = 1

