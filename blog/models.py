from django.db import models


class ArticleModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100)
    content_text = models.TextField(max_length=100_000)
    preview_text = models.CharField(max_length=130)
    content_image = models.ImageField(upload_to='content_images/')
    preview_image = models.ImageField(upload_to='preview_images/')

    class Meta:
        ordering = ('-created_at', )
