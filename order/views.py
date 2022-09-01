from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from rest_framework.views import APIView
from rest_framework.response import Response

from . import models
from . import serializers
from . import forms
from utils import PopupCookiesContextMixin


class BoardAPIView(APIView):
    def get(self, request):
        board = models.Board.objects.last()
        return Response(serializers.BoardSerializer(board).data)


class CreateOrderCalcPageView(PopupCookiesContextMixin, LoginRequiredMixin, CreateView):
    template_name = 'order/order-dms.html'
    success_url = reverse_lazy('order_step_two')
    model = models.OrderCalcModel
    form_class = forms.CreateOrderCalcForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = 'order'
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class CreateOrderPageView(PopupCookiesContextMixin, LoginRequiredMixin, CreateView):
    template_name = 'order/order-dms-step-2.html'
    success_url = reverse_lazy('home')
    model = models.OrderModel
    form_class = forms.CreateOrderForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = 'order'

        last_order_calc = models.OrderCalcModel.objects.last()
        context['social_network'] = last_order_calc.social_network
        context['amount'] = last_order_calc.amount
        context['total_price'] = last_order_calc.total
        return context

    def form_valid(self, form):
        form.instance.order_calc = models.OrderCalcModel.objects.last()
        return super().form_valid(form)


class OrderActivePageView(PopupCookiesContextMixin, LoginRequiredMixin, TemplateView):
    template_name = 'order/order-active.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = 'order_active'
        return context


class OrderHistoryPageView(PopupCookiesContextMixin, LoginRequiredMixin, TemplateView):
    template_name = 'order/order-history.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = 'order_history'
        return context
