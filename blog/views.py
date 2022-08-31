from django.views.generic import DetailView

from .models import ArticleModel
from utils import PopupCookiesContextMixin, PopupAuthContextMixin


class BlogPageView(PopupCookiesContextMixin, PopupAuthContextMixin, DetailView):
    model = ArticleModel
    template_name = 'blog/blog.html'
    pk_url_kwarg = 'page_pk'
    context_object_name = 'page_pk'

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
        context['current_page_is_divided_into_3'] = True if not page_pk % 3 else False
        context['current_page_pk_is_even'] = True if not page_pk % 2 else False
        return context


class ArticlePageView(PopupCookiesContextMixin, PopupAuthContextMixin, DetailView):
    model = ArticleModel
    template_name = 'blog/article-page.html'
    pk_url_kwarg = 'article_pk'
    context_object_name = 'article'
