from django.views.generic import DetailView, ListView
from django.http import Http404

from .models import ArticleModel

from utils import PopupCookiesContextMixin
from utils import PopupAuthContextMixin
from utils import MetaInfoContextMixin


class BlogPageView(MetaInfoContextMixin, PopupCookiesContextMixin, PopupAuthContextMixin, ListView):
    template_name = 'blog/blog.html'
    model = ArticleModel
    context_object_name = 'articles'
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = 'blog'
        return context


class ArticlePageView(PopupCookiesContextMixin, PopupAuthContextMixin, DetailView):
    model = ArticleModel
    template_name = 'blog/article-page.html'
    slug_url_kwarg = 'article_slug'
    context_object_name = 'article'

    def get_object(self):
        return self.model.objects.get(slug=self.kwargs.get(self.slug_url_kwarg))

    def get_context_data(self, **kwargs):
        article = self.model.objects.get(slug=self.kwargs.get(self.slug_url_kwarg))
        context = super().get_context_data(**kwargs)

        context['page'] = 'blog'
        context['title'] = article.meta_title
        context['description'] = article.meta_description
        return context
