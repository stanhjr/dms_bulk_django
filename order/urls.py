from django.urls import path

from . import views


urlpatterns = [
    path('', views.CreateOrderCalcPageView.as_view(), name='order'),
    path('step_two/', views.SetCompaignInfoPageView.as_view(),
         name='order_step_two'),
    path('step_tree/', views.OrderModelCreateView.as_view(), name='order_step_tree'),
    path('active/', views.OrderActivePageView.as_view(), name='order_active'),
    path('history/', views.OrderHistoryPageView.as_view(), name='order_history'),
    path('board/', views.BoardAPIView.as_view()),
    path('statistics/<slug:slug>',
         views.StatisticsApiView.as_view(), name='statistics'),
]
