from django.urls import path

from . import views


urlpatterns = [
    path('', views.MainPageView.as_view(), name='home'),
    path('accept_cookies_policy/', views.AcceptCookiesPolicy.as_view(), name='accept_cookies_policy'),
    path('cookies_policy/', views.CookiesPolicyPageView.as_view(), name='cookies_policy'),
    path('loyalty_program/', views.LoyaltyProgramPageView.as_view(), name='loyalty_program'),
    path('faq/', views.FAQPageView.as_view(), name='faq'),
    path('contacts/', views.ContactsPageView.as_view(), name='contacts'),
]
