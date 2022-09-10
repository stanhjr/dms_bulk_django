from django.views.generic.base import TemplateView, View
from django.shortcuts import redirect
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import get_user_model
from django.contrib import messages

from account_auth.forms import SignUpForm
from account_auth.forms import SignInForm

from utils import PopupCookiesContextMixin
from utils import PopupAuthContextMixin

from email_sender import send_verify_link_to_email
from email_sender import generate_key


class MainPageView(PopupCookiesContextMixin, PopupAuthContextMixin, TemplateView):
    template_name = 'home/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = 'home'
        return context

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
                else:
                    messages.warning(self.request, 'such email is not registered or the password does not match')
                    return redirect('home')
            else:
                messages.warning(self.request, 'such email is not registered or the password does not match')
                return redirect('home')

        if action == 'sign_up_form':
            sign_up_form = SignUpForm(request.POST or None)

            if sign_up_form.is_valid():
                sign_up_form.save()
                username = sign_up_form.cleaned_data.get('username')
                password = sign_up_form.cleaned_data.get('password1')
                new_user = authenticate(username=username, password=password)

                if new_user:
                    new_user.verify_code = generate_key()
                    send_verify_link_to_email.delay(new_user.verify_code, sign_up_form.cleaned_data.get("email"))
                    new_user.save()
                    login(request, new_user)
                    return redirect('dashboard')
                else:
                    messages.warning(self.request, 'the entered passwords do not match')
                    return redirect('home')
            else:
                messages.warning(self.request, 'the entered passwords do not match')
                return redirect('home')

        return redirect('home')


class AcceptCookiesPolicy(View):
    def post(self, request):
        request.session['cookies_policy_accepted'] = True

        # it's not required redirect, form redirects to hidden iframe
        return redirect('home')


class CookiesPolicyPageView(PopupCookiesContextMixin, PopupAuthContextMixin, TemplateView):
    template_name = 'home/cookies-policy.html'


class FAQPageView(PopupCookiesContextMixin, PopupAuthContextMixin, TemplateView):
    template_name = 'home/faq.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = 'faq'
        return context


class LoyaltyProgramPageView(PopupCookiesContextMixin, PopupAuthContextMixin, TemplateView):
    template_name = 'home/loyalty-program.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = 'loyalty_program'
        return context
