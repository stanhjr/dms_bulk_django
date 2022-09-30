from django.urls import path
from django.contrib.sitemaps.views import sitemap
from django.contrib.sitemaps import GenericSitemap

from blog.models import ArticleModel

from . import views

articles_model_info = {
    'queryset': ArticleModel.objects.all(),
    'date_field': 'updated_at'
}

urlpatterns = [
    path('<int:page_pk>/', views.BlogPageView.as_view(), name='blog'),
    path('article/<slug:article_slug>/', views.ArticlePageView.as_view(), name='article'),
    path('sitemap.xml', sitemap,
         {'sitemaps': {'blog': GenericSitemap(articles_model_info, priority=0.5)}},
         name='django.contrib.sitemaps.views.sitemap'),
]
