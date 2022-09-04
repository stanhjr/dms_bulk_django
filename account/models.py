from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Q


class CustomUser(AbstractUser):
    receive_news = models.BooleanField(default=True)
    receive_activity = models.BooleanField(default=True)

    dms_tokens = models.BigIntegerField(default=0)
    cents = models.BigIntegerField(default=0)

    @property
    def is_active_order(self):
        from order.models import OrderModel
        q1 = Q(scraping=True)
        q2 = Q(filtering=True)
        q3 = Q(sending=True)
        if OrderModel.objects.filter(order_calc__user=self).filter(q1 | q2 | q3).count():
            return True
        return False
