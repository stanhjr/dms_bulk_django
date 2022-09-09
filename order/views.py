from datetime import datetime, timezone, timedelta
from django.views.generic import ListView, CreateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.db import transaction, models
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import OrderModel, OrderCalcModel, BoardModel
from . import serializers
from . import forms
from utils import PopupCookiesContextMixin


class BoardAPIView(APIView):
    def get(self, request):
        board = BoardModel.objects.last()
        return Response(serializers.BoardSerializer(board).data)


class StatisticsApiView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, slug):

        REQUIRED_API_DATA_LENGTH = 7

        q1 = Q(order_calc__social_network=slug.capitalize())
        q2 = Q(order_calc__user=request.user)
        q3 = Q(sending=True)
        user_orders = OrderModel.objects.filter(q1 & q2 & q3).values('sending_end_at__date').order_by(
            'sending_end_at__date').annotate(sum=models.Sum('order_calc__amount_integer'))[:7]

        amount_data = [i['sum'] for i in user_orders]
        categories_data = [datetime.now() - timedelta(days=i)
                           for i in range(REQUIRED_API_DATA_LENGTH)]
        categories_data = [i.strftime('%-d %B') for i in categories_data]

        data_example = {
            'data': [0] * (REQUIRED_API_DATA_LENGTH - len(user_orders)) + amount_data,
            'categories': reversed(categories_data)
        }
        return Response(data_example)


class CreateOrderCalcPageView(PopupCookiesContextMixin, LoginRequiredMixin, CreateView):
    template_name = 'order/order-dms.html'
    success_url = reverse_lazy('order_step_two')
    model = OrderCalcModel
    form_class = forms.CreateOrderCalcForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = 'order'
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class OrderModelCreateView(PopupCookiesContextMixin, LoginRequiredMixin, CreateView):
    model = OrderModel
    template_name = 'order/order-dms-step-3.html'
    form_class = forms.CreateOrderForm
    unsuccess_url = reverse_lazy('order_step_two')
    success_url = reverse_lazy('order_active')

    def form_invalid(self):
        return redirect(self.unsuccess_url)

    def form_valid(self, form):
        obj = form.save(commit=False)

        order_calc = OrderCalcModel.objects.last()
        board = BoardModel.objects.last()

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


class SetCompaignInfoPageView(PopupCookiesContextMixin, LoginRequiredMixin, TemplateView):
    template_name = 'order/order-dms-step-2.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = 'order'

        last_order_calc = OrderCalcModel.objects.last()
        context['social_network'] = last_order_calc.social_network
        context['amount'] = last_order_calc.amount
        context['total_price'] = last_order_calc.total
        return context


class OrderActivePageView(PopupCookiesContextMixin, LoginRequiredMixin, ListView):
    template_name = 'order/order-active.html'
    model = OrderModel
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
    model = OrderModel
    context_object_name = 'completed_orders'

    def get_queryset(self):
        return self.model.objects.filter(order_calc__user=self.request.user).filter(completed=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = 'order_history'
        return context
