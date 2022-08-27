from django.views.generic.edit import UpdateView
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy

from .forms import EmailSettingsForm, CustomPasswordChangeForm
from utils import PopupCookiesContextMixin


class AccountSettingsPageView(PopupCookiesContextMixin, LoginRequiredMixin, TemplateView):
    template_name = 'account/settings.html'
    login_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['page'] = 'settings'

        receive_news_initial = self.request.user.receive_news
        receive_activity_initial = self.request.user.receive_activity
        context['email_settings_form'] = EmailSettingsForm(
            receive_news_initial=receive_news_initial,
            receive_activity_initial=receive_activity_initial)

        context['password_change_form'] = CustomPasswordChangeForm(self.request.user)

        return context


class EmailSettingsUpdateView(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    success_url = reverse_lazy('settings')
    login_url = reverse_lazy('home')
    fields = ['receive_news', 'receive_activity']

    def get_object(self, queryset=None):
        return self.request.user