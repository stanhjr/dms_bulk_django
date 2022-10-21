from datetime import datetime
from datetime import timezone
from datetime import timedelta

from django.views.generic import ListView
from django.views.generic import CreateView
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.db import transaction, models
from django.db.models import Q

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import BoardModel, Coupon
from .models import OrderCalcModel
from .models import OrderModel

from . import serializers
from . import forms
from .tools import get_total_price
from .utils import ConfirmRequiredMixin, calculate_amount_integer
from utils import PopupCookiesContextMixin, ServicesUnderMaintenanceDataMixin, MetaInfoContextMixin


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
        categories_data = [i.strftime('%-d %b') for i in categories_data]

        data_example = {
            'data': [0] * (REQUIRED_API_DATA_LENGTH - len(user_orders)) + amount_data,
            'categories': reversed(categories_data)
        }
        return Response(data_example)


class CreateOrderCalcPageView(MetaInfoContextMixin, ServicesUnderMaintenanceDataMixin, PopupCookiesContextMixin, ConfirmRequiredMixin, LoginRequiredMixin, CreateView):
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
        form.cleaned_data['amount_integer'] = calculate_amount_integer(
            amount=form.cleaned_data.get('amount'))
        return super().form_valid(form)


class OrderModelCreateView(MetaInfoContextMixin, PopupCookiesContextMixin, ConfirmRequiredMixin, LoginRequiredMixin, CreateView):
    model = OrderModel
    template_name = 'order/order-dms-step-3.html'
    form_class = forms.CreateOrderForm
    unsuccess_url = reverse_lazy('dashboard')
    success_url = reverse_lazy('order_active')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        last_order_calc = OrderCalcModel.objects.last()
        context['page'] = 'order'
        context['total_price'] = last_order_calc.total
        return context

    def form_invalid(self, form):
        return redirect(self.unsuccess_url)

    def form_valid(self, form):
        print(0)
        obj = form.save(commit=False)
        order_calc = OrderCalcModel.objects.filter(
            user=self.request.user).last()
        board = BoardModel.objects.last()

        order_discount = order_calc.discount
        order_amount = order_calc.amount
        order_total_price = order_calc.total
        try:
            if order_calc.social_network == 'Instagram':
                print(1)
                total_price_index = board.instagram_board_total.index(
                    order_total_price)
                if board.instagram_board_discount[total_price_index] != order_discount:
                    return self.form_invalid()
                if board.instagram_board_amount[total_price_index] != order_amount:
                    return self.form_invalid()

            if order_calc.social_network == 'Twitter':
                print(2)
                total_price_index = board.twitter_board_total.index(
                    order_total_price)
                if board.twitter_board_discount[total_price_index] != order_discount:
                    return self.form_invalid()
                if board.twitter_board_amount[total_price_index] != order_amount:
                    return self.form_invalid()

            if order_calc.social_network == 'Discord':
                print(3)
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

        order_total_price = float(order_total_price[:-1])
        use_dms_tokens = form.cleaned_data.get('use_dms_tokens')

        if use_dms_tokens:
            order_total_price -= self.request.user.dms_tokens

        if order_total_price < 0 and use_dms_tokens:
            self.request.user.dms_tokens = int(abs(order_total_price))
            order_total_price = 0
        else:
            self.request.user.dms_tokens = 0

        coupon = Coupon.objects.filter(name=self.request.POST.get('coupon'), number_of_uses__gte=1) \
            .exclude(user=self.request.user).first()
        if coupon:
            order_total_price *= coupon.get_discount_modifier()
            coupon.number_of_uses -= 1
            coupon.uses += 1

        self.request.user.cents -= order_total_price * 100
        if int(order_total_price * 0.02) < 1:
            self.request.user.dms_tokens += 1
        else:
            self.request.user.dms_tokens += int(
                order_total_price * 0.02)

        obj.order_calc = order_calc
        with transaction.atomic():
            self.request.user.save()
            obj.save()
            if coupon:
                coupon.user.add(self.request.user)
                coupon.save()
        return redirect(self.success_url)


class SetCompaignInfoPageView(MetaInfoContextMixin, PopupCookiesContextMixin, ConfirmRequiredMixin, LoginRequiredMixin, TemplateView):
    template_name = 'order/order-dms-step-2.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = 'order'

        last_order_calc = OrderCalcModel.objects.last()
        context['social_network'] = last_order_calc.social_network
        context['amount'] = last_order_calc.amount
        context['total_price'] = last_order_calc.total
        return context


class OrderActivePageView(MetaInfoContextMixin, PopupCookiesContextMixin, ConfirmRequiredMixin, LoginRequiredMixin, ListView):
    template_name = 'order/order-active.html'
    model = OrderModel
    context_object_name = 'orders'

    def get_queryset(self):
        q1 = Q(order_calc__user=self.request.user)
        q2 = Q(completed=False)
        return self.model.objects.filter(q1 & q2)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = 'order_active'
        context['current_time'] = datetime.now(timezone.utc)
        return context


class OrderHistoryPageView(MetaInfoContextMixin, PopupCookiesContextMixin, ConfirmRequiredMixin, LoginRequiredMixin, ListView):
    template_name = 'order/order-history.html'
    model = OrderModel
    context_object_name = 'completed_orders'

    def get_queryset(self):
        q1 = Q(order_calc__user=self.request.user)
        q2 = Q(completed=True)
        return self.model.objects.filter(q1 & q2)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = 'order_history'
        return context


class GetCouponAPIView(APIView):
    def get(self, request):
        try:
            token = True if request.GET.get("token") == 'true' else False
            if not request.GET.get("token") and not request.GET.get("coupon"):
                return Response(status=404)

            total_price = get_total_price(user=self.request.user,
                                          coupon=request.GET.get("coupon"),
                                          token=token)
            return Response({"total_price": total_price}, status=200)
        except Exception as e:
            print(e)
            return Response(status=404)
