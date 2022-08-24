from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView


class LoginCustomRequiredMixin:
    """Verify that the current user is authenticated."""

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy('home') + '#popup-login')
        return super().dispatch(request, *args, **kwargs)


class DashboardView(LoginCustomRequiredMixin, TemplateView):
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Dashboard'
        return context
