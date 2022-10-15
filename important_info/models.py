from typing import Tuple

from django.core.exceptions import ValidationError
from django.db import models


class FAQModel(models.Model):
    question = models.CharField(max_length=90)
    answer = models.TextField(max_length=1000)

    class Meta:
        verbose_name = 'Faq settings'
        verbose_name_plural = 'Faq settings'


class PageModel(models.Model):
    slug = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=500)

    def __str__(self):
        return self.title

    @classmethod
    def get_meta_info(cls, slug: str = '') -> Tuple[str, str]:
        """Used for getting title and description for page with specify slug"""

        last_page_meta = cls.objects.filter(slug=slug).last()
        if not last_page_meta:
            return '', ''
        return last_page_meta.title, last_page_meta.description

    class Meta:
        verbose_name = 'Page Seo Settings'
        verbose_name_plural = 'Pages Seo Settings'


class SeoText(models.Model):
    name_for_admin = models.CharField(max_length=200, default='default name')
    text = models.TextField()
    sorted_text = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('sorted_text',)
        verbose_name = 'Seo Text'
        verbose_name_plural = 'Seo Text'

    def __str__(self):
        return self.name_for_admin


class SeoTitle(models.Model):
    title = models.CharField(max_length=2000)

    class Meta:
        verbose_name = 'Seo Title'
        verbose_name_plural = 'Seo Title'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.pk and SeoTitle.objects.exists():
            raise ValidationError('There is can be only one SeoTitle instance')
        return super(SeoTitle, self).save(*args, **kwargs)
