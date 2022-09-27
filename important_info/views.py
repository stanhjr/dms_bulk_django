from django.views.generic import TemplateView, ListView, View
from django.shortcuts import redirect

from utils import PopupCookiesContextMixin
from utils import PopupAuthContextMixin
from utils import MetaInfoContextMixin

from important_info.models import FAQModel


class CookiesPolicyPageView(MetaInfoContextMixin, PopupCookiesContextMixin, PopupAuthContextMixin, TemplateView):
    template_name = 'policy/cookies-policy.html'
    page_slug = 'cookies-policy'


class FAQPageView(MetaInfoContextMixin, PopupCookiesContextMixin, PopupAuthContextMixin, ListView):
    template_name = 'policy/faq.html'
    model = FAQModel
    context_object_name = 'questions'
    page_slug = 'faq'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = 'faq'
        return context


class AcceptCookiesPolicy(View):
    def post(self, request):
        request.session['cookies_policy_accepted'] = True

        # it's not required redirect, form redirects to hidden iframe
        return redirect('home')


class PrivacyPolicyPageView(MetaInfoContextMixin, PopupCookiesContextMixin, PopupAuthContextMixin, TemplateView):
    template_name = 'policy/privacy-policy.html'
    page_slug = 'privacy-policy'


class RulesPageView(MetaInfoContextMixin, PopupCookiesContextMixin, PopupAuthContextMixin, TemplateView):
    template_name = 'policy/rules.html'
    page_slug = 'rules'


class ForEUCitizens(MetaInfoContextMixin, PopupCookiesContextMixin, PopupAuthContextMixin, TemplateView):
    template_name = 'policy/for-eu-citizens.html'
    page_slug = 'for-eu-citizens'
