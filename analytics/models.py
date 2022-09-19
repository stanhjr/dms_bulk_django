from django.db import models

from order.models import BoardModel


class GoogleAnalytics(BoardModel):
    class Meta:
        proxy = True
        verbose_name = 'Google Analytics'
        verbose_name_plural = 'Google Analytics'


class UserStatistics(models.Model):
    created_at = models.DateField(auto_now_add=True)
    visitors_number = models.BigIntegerField(null=True)

