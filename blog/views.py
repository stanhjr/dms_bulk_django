from django.views.generic import ListView, DetailView

from .models import ArticleModel
from utils import PopupCookiesContextMixin, PopupAuthContextMixin


class BlogPageView(PopupCookiesContextMixin, PopupAuthContextMixin, ListView):
    model = ArticleModel
    template_name = 'blog/blog.html'
    context_object_name = 'articles_previews'


class ArticlePageView(PopupCookiesContextMixin, PopupAuthContextMixin, DetailView):
    model = ArticleModel
    template_name = 'blog/article-page.html'
    pk_url_kwarg = 'article_pk'
    context_object_name = 'article'
    