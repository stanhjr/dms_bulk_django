from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.views import APIView
from rest_framework.response import Response

from . import models
from . import serializers
from utils import PopupCookiesContextMixin


class BoardAPIView(APIView):
    def get(self, request):
        board = models.Board.objects.get(pk=1)
        return Response(serializers.BoardSerializer(board).data)


class OrderDMSPageView(PopupCookiesContextMixin, LoginRequiredMixin, TemplateView):
    template_name = 'order/order-dms.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = 'order'
        return context


class OrderDMSStepTwoPageView(PopupCookiesContextMixin, LoginRequiredMixin, TemplateView):
    template_name = "order/order-dms-step-2.html"


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
