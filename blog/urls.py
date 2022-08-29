from django.urls import path

from . import views


urlpatterns = [
    path('', views.BlogPageView.as_view(), name='blog'),
    path('article/<int:article_pk>', views.ArticlePageView.as_view(), name='article'),
]