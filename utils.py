from django.views.generic.base import ContextMixin

from account_auth.forms import SignUpForm, SignInForm
from order.models import ServicesUnderMaintenance
from home.models import PageModel


class PopupCookiesContextMixin(ContextMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cookies_policy_accepted'] = self.request.session.get('cookies_policy_accepted')
        return context


class ServicesUnderMaintenanceDataMixin(ContextMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['services_under_maintenance'] = ServicesUnderMaintenance.objects.first()
        return context


class PopupAuthContextMixin(ContextMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sign_up_form'] = SignUpForm
        context['sign_in_form'] = SignInForm
        return context


class MetaInfoContextMixin(ContextMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'], context['description'] = PageModel.get_meta_info(self.page_slug)
        return context