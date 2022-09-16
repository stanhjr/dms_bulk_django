import datetime
from urllib.parse import urlparse

import stripe
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.loader import render_to_string
from django.views.generic import CreateView

from djstripe.models import Customer
from djstripe import webhooks

from rest_framework.response import Response
from rest_framework.views import APIView

from django.urls import reverse, reverse_lazy

from account.models import CustomUser
from dms_bulk_django import settings
from dms_bulk_django.settings import STRIPE_TEST_SECRET_KEY
from payment.forms import CreateInvoiceCalcForm
from payment.models import Invoice

PLAN = {
    "stripe": "price_1LgklwK6rkKpcwrptBXibwai",
    "paypal": "some_code",
}


class InvoiceCreateView(LoginRequiredMixin, CreateView):
    model = Invoice
    form_class = CreateInvoiceCalcForm
    success_url = reverse_lazy('add_funds')
    login_url = reverse_lazy('home')

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()


class GetSessionIdAPIView(APIView):
    def get(self, request):

        customer = Customer.objects.get(subscriber=request.user)
        price = int(request.GET.get("price"))
        if not price:
            return Response(status=404)
        stripe.api_key = STRIPE_TEST_SECRET_KEY

        try:
            product = stripe.Product.create(name="Gold Special")
            price = stripe.Price.create(
                product=product.id, unit_amount=price, currency="usd")

            invoice = stripe.Invoice.create(
                customer=customer.id,
                pending_invoice_items_behavior='exclude',
                collection_method="send_invoice",
                days_until_due=30,
            )

            invoice_item = stripe.InvoiceItem.create(
                customer=customer.id,
                price=price.id,
                currency='usd',
                invoice=invoice.id,
            )
            invoice = stripe.Invoice.finalize_invoice(invoice.id)

            data = {
                "session_id": invoice.id,
                "invoice_url": invoice.hosted_invoice_url,
            }
        except stripe.error.InvalidRequestError as e:
            print(e)
            return Response(status=404)

        return Response(data, status=200)


@webhooks.handler("invoice.paid")
def my_handler(event, **kwargs):
    user = event.customer.subscriber
    paid = event.data["object"]["amount_paid"]
    user.cents += int(paid)
    user.save()


class GetPaypalFormPIView(APIView):
    def get(self, request):
        try:
            price = float(request.GET.get("price"))
            client_id = settings.PAYPAL_CLIENT_ID
        except Exception as e:
            print(e)
            return Response(status=404)
        invoice_id = "ARv3ot_OU4zgMCM_vZ3Xgb0c0ovmFfL_pRRrIlLxPWuq7nZMUUvO2PHS9cCoa1eYNt9G1apgJxyUwqbr"
        paypal_dict = {
            "business": settings.PAYPAL_RECEIVER_EMAIL,
            "amount": price,
            "item_name": "name of the item",
            "invoice": invoice_id,
            "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
            "return": request.build_absolute_uri(reverse('add_funds')),
            "cancel_return": request.build_absolute_uri(reverse('add_funds')),
            # Custom command to correlate to some function later (optional)
            "custom": "premium_plan",
        }
        form = CustomPayPalPaymentsForm(initial=paypal_dict)
        content = render_to_string(
            "popup/paypal_invoice.html",
            request=request,
            context={
                'form': form,
                'date_now': datetime.datetime.now().strftime("%d.%m.%Y"),
                'pay_method': 'Paypal',
                'invoice_id': invoice_id,
                "price": price,
                "client_id": client_id,
            }
        )

        return Response({"content": content}, status=200)


class PaypalAPIView(APIView):
    def post(self, request):
        url = urlparse(request.META.get("HTTP_PAYPAL_CERT_URL"))

        if url.hostname == 'api.paypal.com':
            print('=============')
            print("hostname paypal", True)
        else:
            print("hostname paypal", False)

        if self.request.data.get('event_type') != 'CHECKOUT.ORDER.APPROVED':
            print('NOT APPROVED')
            return Response({"status": "SUCCESSFUL"}, status=200)
        for i, k in self.request.data.items():
            print(i, k)
        resource = self.request.data['resource']
        user_id = resource['purchase_units'][0]['reference_id']
        currency = resource['purchase_units'][0]['amount']['currency_code']
        value = resource['purchase_units'][0]['amount']['value']
        create_time = resource.get("create_time")
        payer_email = resource['payer']['email_address']
        payer_id = resource['payer']['payer_id']
        invoice_id = resource['invoice_id']
        print(user_id, value, currency)
        user = CustomUser.objects.filter(pk=user_id).first()
        if not user:
            return Response({"status": "SUCCESSFUL"}, status=200)

        user.cents += float(value) * 100
        user.save()

        return Response({"status": "SUCCESSFUL"}, status=200)
