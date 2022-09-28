from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.urls import reverse_lazy

from utils import PopupCookiesContextMixin
from utils import MetaInfoContextMixin

from order import models


class DashboardPageView(MetaInfoContextMixin, PopupCookiesContextMixin, LoginRequiredMixin, ListView):
    template_name = 'dashboard/dashboard.html'
    login_url = reverse_lazy('home')
    model = models.OrderModel
    context_object_name = 'recent_orders'
    page_slug = '/dashboard/'

    def get_queryset(self):
        return self.model.objects.filter(order_calc__user=self.request.user)[:3]

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
