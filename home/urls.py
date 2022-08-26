from django.urls import path

from . import views


urlpatterns = [
    path('', views.MainPageView.as_view(), name='home'),
    path('cookies_policy/', views.CookiesPolicyPageView.as_view(), name='cookies_policy')
]