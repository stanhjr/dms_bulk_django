from django.urls import path

from . import views

urlpatterns = [
    path('info-accept-cookies-policy/', views.AcceptCookiesPolicy.as_view(),
         name='accept_cookies_policy'),
    path('info-cookies-policy/', views.CookiesPolicyPageView.as_view(),
         name='cookies_policy'),
    path('info-privacy-policy/', views.PrivacyPolicyPageView.as_view(),
         name='privacy_policy'),
    path('info-rules/', views.RulesPageView.as_view(), name='rules'),
    path('info-for-eu-citizens/', views.ForEUCitizens.as_view(), name='for_eu_citizens'),
    path('info-faq/', views.FAQPageView.as_view(), name='faq'),
]
