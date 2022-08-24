from django.views.generic.base import TemplateView
from django.shortcuts import render
from django.http import HttpResponse

from account_auth.forms import SignUpForm


class MainPageView(TemplateView):
    template_name = 'index.html'
    sign_up_form = SignUpForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['sign_up_form'] = self.sign_up_form

        return context

    def post(self, request):
        sign_up_form = SignUpForm(request.POST)

        if sign_up_form.is_valid():
            sign_up_form.save()
            return render(request, 'index.html')
        return HttpResponse('The Woooorudo!')