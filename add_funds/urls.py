from django.urls import path

from . import views


urlpatterns = [
    path('', views.AddFundsPageView.as_view(), name='add_funds'),
    path('create_invoice_calc/', views.InvoiceCreateView.as_view(),
         name='create_invoice_calc')
]
