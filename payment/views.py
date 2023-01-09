from urllib.parse import urlparse

import stripe
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import HttpResponse

from django.utils import timezone

from django.views.generic import CreateView, TemplateView

from djstripe.models import Customer
from djstripe import webhooks
from rest_framework.permissions import IsAuthenticated

from rest_framework.response import Response
from rest_framework.views import APIView

from django.urls import reverse_lazy

from account.models import CustomUser
from dms_bulk_django import settings
from dms_bulk_django.settings import STRIPE_TEST_SECRET_KEY
from payment.forms import CreateInvoiceCalcForm
from payment.models import Invoice
from celery_tasks import send_balance_update
from django.template.loader import render_to_string
from coinbase_commerce.client import Client
from coinbase_commerce.error import SignatureVerificationError, WebhookInvalidPayload
from coinbase_commerce.webhook import Webhook
from django.shortcuts import render

from utils import MetaInfoContextMixin

PLAN = {
    "stripe": "price_1LgklwK6rkKpcwrptBXibwai",
    "paypal": "some_code",
}


class InvoiceCreateView(MetaInfoContextMixin, LoginRequiredMixin, CreateView):
    model = Invoice
    form_class = CreateInvoiceCalcForm
    success_url = reverse_lazy('add_funds')
    login_url = reverse_lazy('home')

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()


class GetSessionIdAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        customer = Customer.objects.get(subscriber=self.request.user)
        try:
            price = int(float(request.GET.get("price"))) * 100
            invoice_model = Invoice.objects.filter(invoice_id=request.GET.get("invoice_id")).first()
        except ValueError:
            return Response(status=404)
        if not price or not invoice_model:
            return Response(status=404)
        stripe.api_key = STRIPE_TEST_SECRET_KEY

        try:
            product = stripe.Product.create(name="Social Media Marketing")
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
            invoice_model.stripe_invoice_id = invoice.id
            invoice_model.save()
        except stripe.error.InvalidRequestError as e:
            print(e)
            return Response(status=404)

        return Response(data, status=200)


@webhooks.handler("invoice.paid")
def my_handler(event, **kwargs):
    user = event.customer.subscriber
    paid = event.data["object"]["amount_paid"]
    invoice = Invoice.objects.filter(stripe_invoice_id=event.data["object"]["id"]).first()
    if not invoice:
        return Response(status=404)
    with transaction.atomic():
        invoice.status = 'Paid'
        invoice.complete_at = timezone.now()
        user.cents += int(paid)
        user.save()
        invoice.save()
        send_balance_update.delay(email_to=user.email, cents=user.cents)
    return Response(status=200)


class PaypalAPIView(APIView):
    def post(self, request):
        url = urlparse(request.META.get("HTTP_PAYPAL_CERT_URL"))

        if url.hostname != 'api.paypal.com':
            return Response({"status": "FORBIDDEN"}, status=403)

        if self.request.data.get('event_type') != 'CHECKOUT.ORDER.APPROVED':
            print('NOT APPROVED')
            return Response({"status": "SUCCESSFUL"}, status=200)
        resource = self.request.data['resource']

        user_id = resource['purchase_units'][0]['reference_id']
        currency = resource['purchase_units'][0]['amount']['currency_code']
        value = resource['purchase_units'][0]['amount']['value']
        # create_time = resource.get("create_time")
        # payer_email = resource['payer']['email_address']
        # payer_id = resource['payer']['payer_id']

        print(resource['purchase_units'])

        invoice_id = resource['purchase_units'][0].get('invoice_id')
        if not invoice_id:
            return Response({"status": "SUCCESSFUL"}, status=200)
        print(user_id, value, currency, invoice_id)
        user = CustomUser.objects.filter(pk=user_id).first()
        print(user)
        if not user:
            return Response({"status": "SUCCESSFUL"}, status=200)
        invoice = Invoice.objects.filter(invoice_id=invoice_id).first()
        with transaction.atomic():
            invoice.status = 'Paid'
            invoice.complete_at = timezone.now()
            user.cents += int(float(value) * 100)
            user.save()
            invoice.save()
            send_balance_update.delay(email_to=user.email, cents=user.cents)

        return Response({"status": "SUCCESSFUL"}, status=200)


class CoinBaseAPIView(APIView):
    def post(self, request):
        request_data = request.body.decode('utf-8')
        request_sig = request.headers.get('X-CC-Webhook-Signature', None)
        webhook_secret = settings.COINBASE_COMMERCE_WEBHOOK_SHARED_SECRET

        try:
            event = Webhook.construct_event(request_data, request_sig, webhook_secret)
            # List of all Coinbase webhook events:
            # https://commerce.coinbase.com/docs/api/#webhooks

            if event['type'] == 'charge:confirmed':
                print("==========================================")
                print(event)
                print("==========================================")

                payments = event['data']['payments']
                payments = payments[0]
                usd = payments['net']['local']['amount']
                cents = float(usd) * 100
                invoice_id = event['data']['metadata']['custom']
                print(cents)
                print(invoice_id)

        except (SignatureVerificationError, WebhookInvalidPayload) as e:
            print(e)
            return HttpResponse(e, status=400)

        return HttpResponse('ok', status=200)


# class CoinBaseRenderButtonView(TemplateView):
#     template_name = 'add_funds/coinbase_btn.html'
#
#     def get_context_data(self, **kwargs):
#         print(self.request.GET.get('invoice_id'))
#         context = super().get_context_data()
#         context['invoice_id'] = 'ID-3223'
#         return context
#
#     def get(self, request, *args, **kwargs):
#         res = render_to_string(template_name='add_funds/coinbase_btn.html',
#                                context={'invoice_id': 'ID-3223'},
#                                request=request)
#         return HttpResponse(res)
