from django.urls import path

from core import views


urlpatterns = [
    path('robots.txt/', views.RobotsTxtPageView.as_view(), name='robots'),
    path('google59f76306dc2eaed9.html/', views.GoogleTxtPageView.as_view(), name='robots'),

]
