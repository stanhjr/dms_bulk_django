from django.views.generic.base import TemplateView

from .models import ArticleModel
from utils import PopupCookiesContextMixin, PopupAuthContextMixin


class BlogPageView(PopupCookiesContextMixin, PopupAuthContextMixin, TemplateView):
    template_name = 'blog/blog.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['article_previews'] = ArticleModel.objects.all().order_by('-pk')

        return context
    

class ArticlePageView(PopupCookiesContextMixin, PopupAuthContextMixin, TemplateView):
    template_name = 'blog/article-page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['article'] = ArticleModel.objects.get(pk=kwargs.get('article_id'))

        return context
    