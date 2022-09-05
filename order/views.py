from datetime import datetime, timezone
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.db import transaction
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from . import models
from . import serializers
from . import forms
from utils import PopupCookiesContextMixin


class BoardAPIView(APIView):
    def get(self, request):
        board = models.BoardModel.objects.last()
        return Response(serializers.BoardSerializer(board).data)


class StatisticsApiView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, slug):
        # TODO get statistics for user social media

        amount_data = ['0', '0', '0', '0', '0', '0', '0']

        user_orders = models.OrderModel.objects.filter(
            order_calc__user=request.user).filter(order_calc__social_network=slug.capitalize())[:7]
        user_orders_amount = [
            order.order_calc.amount_without_formatting for order in user_orders]

        for order_amount_index in range(len(user_orders_amount)):
            amount_data[order_amount_index] = user_orders_amount[order_amount_index]

        data_example = {
            'data': reversed(amount_data),
            "categories": ["1 June", "2 June", "3 June", "4 June", "5 June", "6 June", "7 June"]
        }
        return Response(data_example)


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
    success_url = reverse_lazy('order_active')
    unsuccess_url = reverse_lazy('order_step_two')
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

    def form_invalid(self):
        return redirect(self.unsuccess_url)

    def form_valid(self, form):
        obj = form.save(commit=False)

        order_calc = models.OrderCalcModel.objects.last()
        board = models.BoardModel.objects.last()

        order_discount = order_calc.discount
        order_amount = order_calc.amount
        order_total_price = order_calc.total
        try:
            if order_calc.social_network == 'Instagram':
                total_price_index = board.instagram_board_total.index(
                    order_total_price)
                if board.instagram_board_discount[total_price_index] != order_discount:
                    return self.form_invalid()
                if board.instagram_board_amount[total_price_index] != order_amount:
                    return self.form_invalid()

            if order_calc.social_network == 'Twitter':
                total_price_index = board.twitter_board_total.index(
                    order_total_price)
                if board.twitter_board_discount[total_price_index] != order_discount:
                    return self.form_invalid()
                if board.twitter_board_amount[total_price_index] != order_amount:
                    return self.form_invalid()

            if order_calc.social_network == 'Discord':
                total_price_index = board.discord_board_total.index(
                    order_total_price)
                if board.discord_board_discount[total_price_index] != order_discount:
                    return self.form_invalid()
                if board.discord_board_amount[total_price_index] != order_amount:
                    return self.form_invalid()

            if order_calc.social_network == 'Telegram':
                total_price_index = board.telegram_board_total.index(
                    order_total_price)
                if board.telegram_board_discount[total_price_index] != order_discount:
                    return self.form_invalid()
                if board.telegram_board_amount[total_price_index] != order_amount:
                    return self.form_invalid()
        except ValueError:
            return self.form_invalid()

        if float(order_total_price[:-1]) > self.request.user.cents / 100:
            return self.form_invalid()

        self.request.user.cents -= float(order_total_price[:-1]) * 100
        self.request.user.dms_tokens += int(
            float(order_total_price[:-1]) * 0.02)
        obj.order_calc = order_calc

        with transaction.atomic():
            self.request.user.save()
            obj.save()
        return redirect(self.success_url)


class OrderActivePageView(PopupCookiesContextMixin, LoginRequiredMixin, ListView):
    template_name = 'order/order-active.html'
    model = models.OrderModel
    context_object_name = 'orders'

    def get_queryset(self):
        return self.model.objects.filter(order_calc__user=self.request.user).filter(completed=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = 'order_active'
        context['current_time'] = datetime.now(timezone.utc)
        return context


class OrderHistoryPageView(PopupCookiesContextMixin, LoginRequiredMixin, ListView):
    template_name = 'order/order-history.html'
    model = models.OrderModel
    context_object_name = 'completed_orders'

    def get_queryset(self):
        return self.model.objects.filter(order_calc__user=self.request.user).filter(completed=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = 'order_history'
        return context
