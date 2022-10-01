from django.urls import path

from core import views


urlpatterns = [
    path('robots.txt/', views.RobotsTxtPageView.as_view(), name='robots'),
]
