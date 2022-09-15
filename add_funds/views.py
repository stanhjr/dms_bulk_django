from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView

from payment.forms import CreateOrderCalcForm
from payment.models import Invoice
from utils import PopupCookiesContextMixin


class AddFundsPageView(PopupCookiesContextMixin, LoginRequiredMixin, TemplateView):
    template_name = 'add_funds/add-funds.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_invoice_form'] = CreateOrderCalcForm
        context['invoices'] = Invoice.objects.filter()
        return context

