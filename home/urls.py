from django.urls import path

from . import views


urlpatterns = [
    path('', views.MainPageView.as_view(), name='home'),
    path('loyalty_program/', views.LoyaltyProgramPageView.as_view(),
         name='loyalty_program'),
    path('contacts/', views.ContactsPageView.as_view(), name='contacts'),
]
