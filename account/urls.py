from django.urls import path, reverse_lazy
from django.contrib.auth.views import PasswordChangeView

from . import views


urlpatterns = [
    path('settings/', views.AccountSettingsPageView.as_view(), name='settings'),
    path('settings/email', views.EmailSettingsUpdateView.as_view(), name='update_email_settings'),
    path('settings/password', PasswordChangeView.as_view(success_url=reverse_lazy('settings')), name='change_password')
]
