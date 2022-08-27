from django.views.generic.base import TemplateView

from utils import PopupCookiesContextMixin, PopupAuthContextMixin


class BlogPageView(PopupCookiesContextMixin, PopupAuthContextMixin, TemplateView):
    template_name = 'home/blog.html'