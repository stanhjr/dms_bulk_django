from django.urls import path

from . import views


urlpatterns = [
    path('order/', views.CreateOrderCalcPageView.as_view(), name='order'),
    path('order-step-two/', views.SetCompaignInfoPageView.as_view(), name='order_step_two'),
    path('order-step-three/', views.OrderModelCreateView.as_view(), name='order_step_three'),
    path('order-active/', views.OrderActivePageView.as_view(), name='order_active'),
    path('order-history/', views.OrderHistoryPageView.as_view(), name='order_history'),
    path('order-board/', views.BoardAPIView.as_view()),
    path('order-statistics/<slug:slug>', views.StatisticsApiView.as_view(), name='statistics'),
    path('order-get-discount/', views.GetCouponAPIView.as_view(), name='get_discount'),
]
