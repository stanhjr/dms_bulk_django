from datetime import datetime, timezone, timedelta

import django
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator
from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone as tz

from celery_tasks.tasks import delete_order_from_actives


class BoardModel(models.Model):
    instagram_board_quantity = ArrayField(models.CharField(max_length=20))
    instagram_board_amount = ArrayField(models.CharField(max_length=20))
    instagram_board_discount = ArrayField(models.CharField(max_length=20))
    instagram_board_total = ArrayField(
        models.CharField(max_length=20), null=True)

    twitter_board_quantity = ArrayField(models.CharField(max_length=20))
    twitter_board_amount = ArrayField(models.CharField(max_length=20))
    twitter_board_discount = ArrayField(models.CharField(max_length=20))
    twitter_board_total = ArrayField(
        models.CharField(max_length=20), null=True)

    discord_board_quantity = ArrayField(models.CharField(max_length=20))
    discord_board_amount = ArrayField(models.CharField(max_length=20))
    discord_board_discount = ArrayField(models.CharField(max_length=20))
    discord_board_total = ArrayField(
        models.CharField(max_length=20), null=True)

    telegram_board_quantity = ArrayField(models.CharField(max_length=20))
    telegram_board_amount = ArrayField(models.CharField(max_length=20))
    telegram_board_discount = ArrayField(models.CharField(max_length=20))
    telegram_board_total = ArrayField(
        models.CharField(max_length=20), null=True)


class OrderCalcModel(models.Model):
    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name='order_calc_model')
    SOCIAL_NETWORK_CHOICES = (
        ('Instagram', 'Instagram'),
        ('Twitter', 'Twitter'),
        ('Discord', 'Discord'),
        ('Telegram', 'Telegram')
    )

    social_network = models.CharField(
        max_length=9, choices=SOCIAL_NETWORK_CHOICES)
    amount = models.CharField(max_length=10)
    amount_integer = models.IntegerField(default=0)
    discount = models.CharField(max_length=10)
    total = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def amount_without_formatting(self):
        amount = int(self.amount[:-1])
        if self.amount[-1] == 'm':
            amount *= 1_000
        return amount

    @property
    def total_price(self):
        return int(self.total.replace("$", ""))

    def __str__(self):
        return f'{self.social_network} by {self.user.username} {self.total}'

    def save(self, *args, **kwargs):
        if self.amount[-1] == 'k':
            self.amount_integer = int(self.amount[:-1])
        if self.amount[-1] == 'm':
            self.amount_integer = int(self.amount[:-1]) * 1_000
        super(OrderCalcModel, self).save(*args, **kwargs)


class OrderModel(models.Model):
    order_calc = models.ForeignKey(
        OrderCalcModel, on_delete=models.CASCADE, related_name='order_model')

    sending_end_at = models.DateTimeField(blank=True, null=True)
    sending_start_at = models.DateTimeField(blank=True, null=True)
    send_messages_speed = models.IntegerField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    targets_or_competitors_submited = models.TextField(
        max_length=100_000)
    use_our_default_filtering = models.BooleanField()
    not_use_any_filtering = models.BooleanField()
    message = models.TextField(max_length=1000)
    attach_in_message = models.TextField(max_length=600)
    additional_information = models.TextField(max_length=600)
    contact_details = models.CharField(max_length=1000)

    scraping = models.BooleanField(default=False)
    filtering = models.BooleanField(default=False)
    sending = models.BooleanField(default=False)

    completed = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.clean()

        if self.sending and not self.completed:
            send_date = datetime.utcnow() + timedelta(days=1)
            delete_order_from_actives.apply_async((self.pk,), eta=send_date)

        if self.filtering and not self.sending:
            self.send_messages_speed = self.__get_send_messages_speed_per_minutes()
            self.sending_start_at = datetime.utcnow()

        return super().save(*args, **kwargs)

    @property
    def time_from_sending_start_at(self):
        return int((datetime.utcnow() - self.sending_start_at).total_seconds())

    def __get_send_messages_speed_per_minutes(self):
        amount = int(self.order_calc.amount[:-1])
        seconds_ago = int((self.sending_end_at -
                           datetime.utcnow()).total_seconds())

        if self.order_calc.amount[-1] == 'k':
            amount *= 1_000
        else:
            amount *= 1_000_000

        return amount / seconds_ago

    def clean(self):
        if self.filtering and not self.scraping:
            raise ValidationError(
                'you must set scraping end status for setting filtering end status')
        if self.filtering and not self.sending_end_at:
            raise ValidationError(
                'you must set sending_end_at before set filtering end status')
        if self.sending_end_at:
            if self.sending_end_at <= datetime.now(timezone.utc) and not self.sending:
                raise ValidationError(
                    'sending_end_at must be later current time')
        if self.sending and not self.filtering:
            raise ValidationError(
                'you must set filtering end status for setting sending end status')

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return f'{self.order_calc} completed={self.completed}'


class Coupon(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=1000)
    discount = models.IntegerField(validators=[MaxValueValidator(100), MinValueValidator(1)])
    number_of_uses = models.IntegerField(default=1)
    user = models.ManyToManyField(get_user_model(), related_name='coupon', null=True, blank=True)

    def get_discount_modifier(self) -> float:
        return (100 - self.discount) / 100

    def __str__(self):
        return f'{self.name}, number_of_uses = {self.number_of_uses}'
