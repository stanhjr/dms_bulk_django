from django.views.generic.base import TemplateView
from django.shortcuts import redirect
from django.contrib.auth import login, authenticate, get_user_model

from account_auth.forms import SignUpForm, SignInForm


class MainPageView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['sign_up_form'] = SignUpForm
        context['sign_in_form'] = SignInForm
        context['title'] = 'Home'

        return context

    def post(self, request):
        action = self.request.POST.get('action')

        if action == 'sign_in_form':
            sign_in_form = SignInForm(request.POST or None)
            if sign_in_form.is_valid():
                email = sign_in_form.cleaned_data.get('email')
                password = sign_in_form.cleaned_data.get('password')
                username = get_user_model().objects.filter(email=email).first().username
                login_user = authenticate(username=username, password=password)

                if login_user:
                    login(request, login_user)
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