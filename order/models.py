from datetime import datetime, timezone
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models


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
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='order_calc_model')
    SOCIAL_NETWORK_CHOICES = (
        ('Instagram', 'Instagram'),
        ('Twitter', 'Twitter'),
        ('Discord', 'Discord'),
        ('Telegram', 'Telegram')
    )

    social_network = models.CharField(
        max_length=9, choices=SOCIAL_NETWORK_CHOICES)
    amount = models.CharField(max_length=10)
    discount = models.CharField(max_length=10)
    total = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.social_network} by {self.user.username} {self.total}'


class OrderModel(models.Model):
    order_calc = models.ForeignKey(OrderCalcModel, on_delete=models.CASCADE, related_name='order_model')

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
        if self.filtering and not self.sending:
            self.send_messages_speed = self.__get_send_messages_speed_per_minutes()
            self.sending_start_at = datetime.now(timezone.utc)
        return super().save(*args, **kwargs)

    @property
    def time_from_sending_start_at(self):
        return int((datetime.now(timezone.utc) - self.sending_start_at).total_seconds())

    def __get_send_messages_speed_per_minutes(self):
        amount = int(self.order_calc.amount[:-1])
        seconds_ago = int((self.sending_end_at -
                           datetime.now(timezone.utc)).total_seconds())

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
        ordering = ('-created_at', )

    def __str__(self):
        return f'{self.order_calc} completed={self.completed}'
