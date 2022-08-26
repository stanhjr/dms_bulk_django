from django.urls import path

from . import views


urlpatterns = [
    path('', views.DashboardPageView.as_view(), name='dashboard'),
]
