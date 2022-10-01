from django.db import models
from django.utils import timezone as tz
from django.urls import reverse_lazy
from slugify import slugify


class ArticleModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, unique=True)
    slug = models.CharField(max_length=150, unique=True, blank=True)
    content_text = models.TextField(max_length=100_000)
    preview_text = models.CharField(max_length=130)
    content_image = models.ImageField(upload_to='content_images/')
    preview_image = models.ImageField(upload_to='preview_images/')

    meta_title = models.CharField(max_length=100, null=True, blank=True)
    meta_description = models.CharField(max_length=500, null=True, blank=True)

    def save(self, *args, **kwargs) -> None:
        if ArticleModel.objects.filter(pk=self.pk):
            self.updated_at = tz.now()
        self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse_lazy('article', kwargs={'article_slug': self.slug})

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Article'
        verbose_name_plural = 'Article'

    def __str__(self):
        return self.title
