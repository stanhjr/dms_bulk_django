from django.urls import path

from . import views


urlpatterns = [
    path('', views.MainPageView.as_view(), name='home'),
    path('loyalty-program/', views.LoyaltyProgramPageView.as_view(),
         name='loyalty_program'),
    path('contacts/', views.ContactsPageView.as_view(), name='contacts'),
    path('telegram/', views.TelegramPageView.as_view(), name='telegram'),
    path('instagram/', views.InstagramPageView.as_view(), name='instagram'),
    path('discord/', views.DiscordPageView.as_view(), name='discord'),
    path('twitter/', views.TwitterPageView.as_view(), name='twitter'),
]
