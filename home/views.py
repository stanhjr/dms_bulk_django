from django.views.generic.base import TemplateView, View
from django.shortcuts import redirect
from django.contrib.auth import login, authenticate, get_user_model

from account_auth.forms import SignUpForm, SignInForm
from utils import PopupCookiesContextMixin, PopupAuthContextMixin


class MainPageView(PopupCookiesContextMixin, PopupAuthContextMixin, TemplateView):
    template_name = 'home/index.html'

    def post(self, request):
        action = self.request.POST.get('action')

        if action == 'sign_in_form':
            sign_in_form = SignInForm(request.POST or None)

            if sign_in_form.is_valid():
                email = sign_in_form.cleaned_data.get('email')
                password = sign_in_form.cleaned_data.get('password')
                remember_me = sign_in_form.cleaned_data.get('remember_me')

                username = get_user_model().objects.get(email=email).username
                login_user = authenticate(username=username, password=password)

                if login_user:
                    login(request, login_user)

                    if not remember_me:
                        request.session.set_expiry(0)

                    return redirect('dashboard')

        if action == 'sign_up_form':
            sign_up_form = SignUpForm(request.POST or None)

            if sign_up_form.is_valid():
                sign_up_form.save()
                username = sign_up_form.cleaned_data.get('username')
                password = sign_up_form.cleaned_data.get('password1')
                new_user = authenticate(username=username, password=password)

                if new_user:
                    login(request, new_user)
                    return redirect('dashboard')

        return redirect('home')


class AcceptCookiesPolicy(View):
    def post(self, request):
        request.session['cookies_policy_accepted'] = True

        # its not required redirect, form redirects to hidden iframe
        return redirect('home')


class CookiesPolicyPageView(PopupCookiesContextMixin, PopupAuthContextMixin, TemplateView):
    template_name = 'home/cookies-policy.html'


class FAQPageView(PopupCookiesContextMixin, PopupAuthContextMixin, TemplateView):
    template_name = 'home/faq.html'