import datetime
from urllib.parse import urlparse

import stripe
from django.template.loader import render_to_string

from djstripe.models import Customer
from djstripe import webhooks

from rest_framework.response import Response
from rest_framework.views import APIView

from django.urls import reverse

from dms_bulk_django.settings import STRIPE_TEST_SECRET_KEY
from payment.forms import CustomPayPalPaymentsForm

PLAN = {
    "stripe": "price_1LgklwK6rkKpcwrptBXibwai",
    "paypal": "some_code",
}


class GetSessionIdAPIView(APIView):
    def get(self, request):

        customer = Customer.objects.get(subscriber=request.user)
        price = int(request.GET.get("price"))
        if not price:
            return Response(status=404)
        stripe.api_key = STRIPE_TEST_SECRET_KEY

        try:
            product = stripe.Product.create(name="Gold Special")
            price = stripe.Price.create(product=product.id, unit_amount=price, currency="usd")

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
        except Exception as e:
            print(e)
            return Response(status=404)
        invoice_id = "unique-invoice-id"
        paypal_dict = {
            "business": "stanhjrpower@gmail.com",
            "amount": price,
            "item_name": "name of the item",
            "invoice": invoice_id,
            "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
            "return": request.build_absolute_uri(reverse('add_funds')),
            "cancel_return": request.build_absolute_uri(reverse('add_funds')),
            "custom": "premium_plan",  # Custom command to correlate to some function later (optional)
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
            }
        )

        return Response({"content": content}, status=200)


class PaypalAPIView(APIView):
    def post(self, request):
        print(self.request.data)
        url = urlparse(request.META.get("HTTP_PAYPAL_CERT_URL"))

        if url.hostname == 'api.paypal.com':
            print('=============')
            print("hostname paypal", True)
        else:
            print("hostname paypal", False)

        price = self.request.data["resource"]["paid_amount"]["paypal"]["value"]
        currency = self.request.data["resource"]["paid_amount"]["paypal"]["currency"]

        print(price, currency)

        return Response({"status": "SUCCESSFUL"}, status=200)
