from django.urls import path

from . import views


urlpatterns = [
    path('', views.AddFundsPageView.as_view(), name='add_funds')
]
