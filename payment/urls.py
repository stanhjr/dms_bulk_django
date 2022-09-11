from django.urls import path

from . import views


urlpatterns = [
    path('stripe/', views.GetSessionIdAPIView.as_view(), name='payment_stripe'),
    path('get_paypal_form/', views.GetPaypalFormPIView.as_view(), name='get_paypal_form'),

]






