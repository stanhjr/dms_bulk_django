from django.urls import path

from . import views


urlpatterns = [
    path('stripe/', views.GetSessionIdAPIView.as_view(), name='payment_stripe'),

]






