from typing import Tuple

from django.db import models


class FAQModel(models.Model):
    question = models.CharField(max_length=90)
    answer = models.TextField(max_length=1000)


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
