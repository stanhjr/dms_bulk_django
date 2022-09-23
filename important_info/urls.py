from django.urls import path

from . import views

urlpatterns = [
    path('accept_cookies_policy/', views.AcceptCookiesPolicy.as_view(),
         name='accept_cookies_policy'),
    path('cookies_policy/', views.CookiesPolicyPageView.as_view(),
         name='cookies_policy'),
    path('privacy_policy/', views.PrivacyPolicyPageView.as_view(),
         name='privacy_policy'),
    path('faq/', views.FAQPageView.as_view(), name='faq'),
]