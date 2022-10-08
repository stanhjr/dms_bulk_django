from django.contrib.sitemaps import Sitemap
from django.urls import reverse_lazy

from blog.models import ArticleModel


class ArticlesSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.5
    protocol = 'https'

    def items(self):
        return ArticleModel.objects.all()

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return obj.get_absolute_url()


class DMSBulkStaticSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.8
    protocol = 'https'

    def items(self):
        return [
            'home',
            'blog',
            'for_eu_citizens',
            'privacy_policy',
            'cookies_policy',
            'rules',
            'faq',
            'loyalty_program',
            'contacts',
        ]

    def location(self, obj):
        if obj == 'blog':
            return reverse_lazy('blog', kwargs={'page_pk': 1})
        return reverse_lazy(obj)

