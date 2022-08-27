from django.views.generic.base import ContextMixin

from account_auth.forms import SignUpForm, SignInForm


class PopupCookiesContextMixin(ContextMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['cookies_policy_accepted'] = self.request.session.get('cookies_policy_accepted')

        return context


class PopupAuthContextMixin(ContextMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['sign_up_form'] = SignUpForm
        context['sign_in_form'] = SignInForm

        return context