from django.views.generic.base import TemplateView
from django.shortcuts import render, redirect

from account_auth.forms import SignUpForm


class MainPageView(TemplateView):
    template_name = 'index.html'
    sign_up_form = SignUpForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['sign_up_form'] = self.sign_up_form
        context['title'] = 'Home'

        return context

    def post(self, request):
        sign_up_form = SignUpForm(request.POST or None)

        if sign_up_form.is_valid():
            sign_up_form.save()
            return redirect('/dashboard')
        return render(request, 'index.html')