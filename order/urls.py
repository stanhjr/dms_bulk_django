from django.urls import path

from . import views


urlpatterns = [
    path('', views.OrderDMSPageView.as_view(), name='order'),
    path('step_two/', views.CreateOrderPageView.as_view(), name='order_step_two'),
    path('active/', views.OrderActivePageView.as_view(), name='order_active'),
    path('history/', views.OrderHistoryPageView.as_view(), name='order_history'),
    path('board/', views.BoardAPIView.as_view())
]
