from django.views.generic.base import TemplateView

from utils import PopupCookiesContextMixin


class OrderDMSPageView(PopupCookiesContextMixin, TemplateView):
    template_name = 'order/order-dms.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['page'] = 'order'

        return context


class OrderActivePageView(PopupCookiesContextMixin, TemplateView):
    template_name = 'order/order-active.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['page'] = 'order_active'

        return context


class OrderHistoryPageView(PopupCookiesContextMixin, TemplateView):
    template_name = 'order/order-history.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['page'] = 'order_history'

        return context