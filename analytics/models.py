from django.db import models

from order.models import BoardModel


class Analytics(BoardModel):
    class Meta:
        proxy = True
        verbose_name = 'Analytics'
        verbose_name_plural = 'Analytics'


class UserStatistics(models.Model):
    created_at = models.DateField(auto_now_add=True)
    visitors_number = models.BigIntegerField(null=True)

