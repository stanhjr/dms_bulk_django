from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.urls import reverse_lazy

from utils import PopupCookiesContextMixin


class DashboardPageView(PopupCookiesContextMixin, LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/dashboard.html'
    login_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['page'] = 'dashboard'
        
        return context

    def post(self, request):
        action = request.POST.get('action')

        if action == 'logout_form':
            logout(request)
            return redirect('home')

        return redirect('dashboard')