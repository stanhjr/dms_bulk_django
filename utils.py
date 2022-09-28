from django.urls import resolve
from django.views.generic.base import ContextMixin

from account_auth.forms import SignUpForm
from account_auth.forms import SignInForm

from order.models import ServicesUnderMaintenance

from important_info.models import PageModel


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
        try:
            current_url = resolve(self.request.path_info).route.split('/')
            if len(current_url) > 1:
                slug = current_url[0]
            else:
                slug = 'home'
        except IndexError:
            slug = 'home'

        context['title'], context['description'] = PageModel.get_meta_info(slug)
        return context
