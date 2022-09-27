from django.views.generic import DetailView
from django.http import Http404

from .models import ArticleModel

from utils import PopupCookiesContextMixin
from utils import PopupAuthContextMixin
from utils import MetaInfoContextMixin


class BlogPageView(MetaInfoContextMixin, PopupCookiesContextMixin, PopupAuthContextMixin, DetailView):
    model = ArticleModel
    template_name = 'blog/blog.html'
    pk_url_kwarg = 'page_pk'
    context_object_name = 'page_pk'
    page_slug = 'blog'

    def get_object(self, queryset=None):
        try:
            return super().get_object(queryset)
        except Http404:
            pass

    def get_context_data(self, **kwargs):
        page_pk = self.kwargs.get('page_pk')

        context = super().get_context_data(**kwargs)
        articles = ArticleModel.objects.all()[(page_pk - 1) * 6:]

        if page_pk * 6 < len(articles):
            articles = articles[:page_pk * 6]

        elif 6 < len(articles):
            articles = articles[:6]

        context['articles_previews'] = articles
        context['current_page_pk'] = page_pk
        context['page'] = 'blog'
        return context


class ArticlePageView(PopupCookiesContextMixin, PopupAuthContextMixin, DetailView):
    model = ArticleModel
    template_name = 'blog/article-page.html'
    pk_url_kwarg = 'article_pk'
    context_object_name = 'article'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = 'blog'
        return context
