from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
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
        order_calc = models.OrderCalcModel.objects.last()
        board = models.BoardModel.objects.last()

        order_discount = order_calc.discount
        order_amount = order_calc.amount
        order_total_price = order_calc.total

        if order_calc.social_network == 'Instagram':
            total_price_index = board.instagram_board_total.index(
                order_total_price)
            if board.instagram_board_discount[total_price_index] != order_discount:
                return
            if board.instagram_board_amount[total_price_index] != order_amount:
                return

        if order_calc.social_network == 'Twitter':
            total_price_index = board.twitter_board_total.index(
                order_total_price)
            if board.twitter_board_discount[total_price_index] != order_discount:
                return
            if board.twitter_board_amount[total_price_index] != order_amount:
                return

        if order_calc.social_network == 'Discord':
            total_price_index = board.discord_board_total.index(
                order_total_price)
            if board.discord_board_discount[total_price_index] != order_discount:
                return
            if board.discord_board_amount[total_price_index] != order_amount:
                return

        if order_calc.social_network == 'Telegram':
            total_price_index = board.telegram_board_total.index(
                order_total_price)
            if board.telegram_board_discount[total_price_index] != order_discount:

                return
            if board.telegram_board_amount[total_price_index] != order_amount:
                return

        if float(order_total_price[:-1]) > self.request.user.cents / 100:
            return

        self.request.user.cents -= float(order_total_price[:-1]) * 100
        self.request.user.save()
        form.instance.order_calc = order_calc
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
