from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, ListView
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect

from payment.forms import CreateInvoiceCalcForm
from payment.models import Invoice
from utils import PopupCookiesContextMixin


class AddFundsPageView(PopupCookiesContextMixin, LoginRequiredMixin, ListView):
    template_name = 'add_funds/add-funds.html'
    model = Invoice
    context_object_name = 'invoices'
    paginate_by = 3

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_invoice_form'] = CreateInvoiceCalcForm
        context['page'] = 'add_funds'
        return context


class InvoiceCreateView(LoginRequiredMixin, CreateView):
    model = Invoice
    success_url = reverse_lazy('add_funds')
    form_class = CreateInvoiceCalcForm

    def form_valid(self, form):
        if not form.cleaned_data.get('cents'):
            messages.warning(
                self.request, 'you cannot add funds for a zero amount')
            return redirect('add_funds')
        form.instance.user = self.request.user
        form.save()
        return super().form_valid(form)


# class AddFundsPageView(PopupCookiesContextMixin, LoginRequiredMixin, ListView):
#     template_name = 'add_funds/add-funds.html'
#     login_url = reverse_lazy('home')
#     model = Invoice
#     context_object_name = 'invoices'

#     def get_queryset(self):
#         return self.model.objects.filter(user=self.request.user)[:3]

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['pages'] = 'add_funds'
#         return context
