from django.shortcuts import redirect
from django.views.generic.edit import UpdateView
from django.views.generic.base import RedirectView
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.contrib.auth import login

from .forms import EmailSettingsForm
from .forms import CustomPasswordChangeForm
from .forms import RestorePasswordChangeForm
from utils import PopupCookiesContextMixin
from .models import CustomUser


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

        if self.request.user.reset_password_code:
            context['password_change_form'] = RestorePasswordChangeForm(
                self.request.user)
            user = self.request.user
            user.reset_password_code = ''
            user.save()
        else:

            context['password_change_form'] = CustomPasswordChangeForm(
                self.request.user)

        return context


class EmailSettingsUpdateView(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    success_url = reverse_lazy('settings')
    login_url = reverse_lazy('home')
    fields = ['receive_news', 'receive_activity']

    def get_object(self, queryset=None):
        return self.request.user


class SignUpConfirm(RedirectView):

    def dispatch(self, request, *args, **kwargs):
        code = self.request.GET.get("code")
        user = CustomUser.objects.filter(code=code).first()
        if user:
            user.verify_code = ''
            user.is_confirmed = True
            user.save()
            return redirect('dashboard')
        else:
            return redirect('home')


class RestorePassword(RedirectView):
    def dispatch(self, request, *args, **kwargs):
        code = self.request.GET.get("code")
        user = CustomUser.objects.filter(reset_password_code=code).first()
        if user:
            login(request=request, user=user)
            return redirect('settings')
        else:
            return redirect('home')
