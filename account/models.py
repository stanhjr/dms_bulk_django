from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Q


class CustomUser(AbstractUser):
    receive_news = models.BooleanField(default=True)
    receive_activity = models.BooleanField(default=True)
    is_confirmed = models.BooleanField(default=False)

    dms_tokens = models.BigIntegerField(default=0)
    cents = models.BigIntegerField(default=0)
    #
    # is_confirm = models.BooleanField(default=False)
    # verify_code = models.CharField(default='', max_length=100)
    # reset_password_code = models.CharField(default='', max_length=100)

    @property
    def is_active_order(self) -> bool:
        """
        Checks if the user has active orders

        :return: bool
        """
        from order.models import OrderModel
        q1 = Q(scraping=True)
        q2 = Q(filtering=True)
        q3 = Q(sending=True)
        return OrderModel.objects.filter(order_calc__user=self).filter(q1 | q2 | q3).exists()
