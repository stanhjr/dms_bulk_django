import random

from django.views.generic import TemplateView
from django.db.models import Q
from django.shortcuts import redirect
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import get_user_model
from django.contrib import messages

from account.models import CustomUser
from account_auth.forms import SignUpForm
from account_auth.forms import SignInForm

from utils import PopupCookiesContextMixin
from utils import PopupAuthContextMixin
from utils import ServicesUnderMaintenanceDataMixin
from utils import MetaInfoContextMixin

from celery_tasks import send_verify_link_to_email
from celery_tasks import generate_key


class MainPageView(MetaInfoContextMixin, ServicesUnderMaintenanceDataMixin, PopupCookiesContextMixin, PopupAuthContextMixin, TemplateView):
    template_name = 'home/index.html'
    page_slug = ''

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

                if not get_user_model().objects.filter(email=email).exists():
                    messages.warning(
                        self.request, 'such email is not registered or the password does not match')
                    return redirect('home')

                username = get_user_model().objects.get(email=email).username
                login_user = authenticate(username=username, password=password)

                if login_user:
                    login(request, login_user)

                    if not remember_me:
                        request.session.set_expiry(0)

                    return redirect('dashboard')
                else:
                    messages.warning(
                        self.request, 'such email is not registered or the password does not match')
                    return redirect('home')
            else:
                messages.warning(
                    self.request, 'such email is not registered or the password does not match')
                return redirect('home')

        if action == 'sign_up_form':
            sign_up_form = SignUpForm(request.POST or None)

            if sign_up_form.is_valid():
                q1 = Q(email=sign_up_form.cleaned_data.get('email'))
                q2 = Q(username=sign_up_form.cleaned_data.get('username'))
                user = CustomUser.objects.filter(q1 | q2).first()

                if user:
                    messages.warning(
                        self.request, 'a user with this email or username already exists')
                    return redirect('home')

                sign_up_form.save()
                username = sign_up_form.cleaned_data.get('username')
                password = sign_up_form.cleaned_data.get('password1')
                new_user = authenticate(username=username, password=password)

                new_user.verify_code = generate_key()
                new_user.avatar_image_id = random.choice((1, 2, 3, 4))
                send_verify_link_to_email.delay(
                    new_user.verify_code, sign_up_form.cleaned_data.get("email"))
                new_user.save()
                login(request, new_user)
                return redirect('dashboard')
            else:
                messages.warning(
                    self.request, 'a user with this email or username already exists')
                return redirect('home')

        return redirect('home')


class LoyaltyProgramPageView(MetaInfoContextMixin, PopupCookiesContextMixin, PopupAuthContextMixin, TemplateView):
    template_name = 'home/loyalty-program.html'
    page_slug = 'loyalty-program'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = 'loyalty_program'
        return context


class ContactsPageView(MetaInfoContextMixin, PopupCookiesContextMixin, PopupAuthContextMixin, TemplateView):
    template_name = 'home/contacts.html'
    page_slug = 'contacts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = 'contacts'
        return context
