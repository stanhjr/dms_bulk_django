from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView
from django.contrib.auth import logout
from django.shortcuts import redirect


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard.html'
    login_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Dashboard'
        context['username'] = self.request.user.username
        return context

    def post(self, request):
        action = request.POST.get('action')

        if action == 'logout_form':
            logout(request)
            return redirect('home')

        return redirect('dashboard')