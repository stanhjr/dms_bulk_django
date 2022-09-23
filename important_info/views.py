from django.views.generic import TemplateView, ListView, View
from django.shortcuts import redirect

from utils import PopupCookiesContextMixin
from utils import PopupAuthContextMixin

from important_info.models import FAQModel


class CookiesPolicyPageView(PopupCookiesContextMixin, PopupAuthContextMixin, TemplateView):
    template_name = 'policy/cookies-policy.html'


class FAQPageView(PopupCookiesContextMixin, PopupAuthContextMixin, ListView):
    template_name = 'policy/faq.html'
    model = FAQModel
    context_object_name = 'questions'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = 'faq'
        return context


class AcceptCookiesPolicy(View):
    def post(self, request):
        request.session['cookies_policy_accepted'] = True

        # it's not required redirect, form redirects to hidden iframe
        return redirect('home')


class PrivacyPolicyPageView(PopupCookiesContextMixin, PopupAuthContextMixin, TemplateView):
    template_name = 'policy/privacy-policy.html'
