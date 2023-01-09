from django.urls import path

from . import views


urlpatterns = [
    path('create-invoice/', views.InvoiceCreateView.as_view(), name='create_invoice'),
    path('stripe/', views.GetSessionIdAPIView.as_view(), name='payment_stripe'),
    path('paypal/', views.PaypalAPIView.as_view(), name='paypal_post'),
    path('coinbase/', views.CoinBaseAPIView.as_view(), name='coinbase'),
    # path('get-btn', views.CoinBaseRenderButtonView.as_view(), name='get-btn'),

]






