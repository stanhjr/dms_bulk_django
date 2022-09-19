from django.db import models

from order.models import BoardModel


class GoogleAnalytics(BoardModel):
    class Meta:
        proxy = True
        verbose_name = 'Google Analytics'
        verbose_name_plural = 'Google Analytics'
