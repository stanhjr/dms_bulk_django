from datetime import timedelta
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator
from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone as tz

from celery_tasks.tasks import delete_order_from_actives
from .utils import calculate_amount_integer


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

    def __str__(self):
        return "Board Settings"

    class Meta:
        verbose_name = 'Board Settings'
        verbose_name_plural = 'Board Settings'

    def __len_telegram(self):
        quantity = len(self.telegram_board_quantity)
        amount = len(self.telegram_board_amount)
        discount = len(self.telegram_board_discount)
        total = len(self.telegram_board_total)
        if (amount, discount, total).count(quantity) == 3:
            return False
        return True

    def __len_twitter(self):
        quantity = len(self.twitter_board_quantity)
        amount = len(self.twitter_board_amount)
        discount = len(self.twitter_board_discount)
        total = len(self.twitter_board_total)
        if (amount, discount, total).count(quantity) == 3:
            return False
        return True

    def __len_discord(self):
        quantity = len(self.discord_board_quantity)
        amount = len(self.discord_board_amount)
        discount = len(self.discord_board_discount)
        total = len(self.discord_board_total)
        if (amount, discount, total).count(quantity) == 3:
            return False
        return True

    def __len_instagram(self):
        quantity = len(self.instagram_board_quantity)
        amount = len(self.instagram_board_amount)
        discount = len(self.instagram_board_discount)
        total = len(self.instagram_board_total)
        if (amount, discount, total).count(quantity) == 3:
            return False
        return True

    def clean(self):
        if not self.__len_instagram():
            raise ValidationError(
                'the length of instagram arrays must be the same')
        if not self.__len_telegram():
            raise ValidationError(
                'the length of telegram arrays must be the same')
        if not self.__len_twitter():
            raise ValidationError(
                'the length of twitter arrays must be the same')
        if not self.__len_discord():
            raise ValidationError(
                'the length of discord arrays must be the same')


class OrderCalcModel(models.Model):
    user = models.OneToOneField(
        get_user_model(), on_delete=models.CASCADE)
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

    @classmethod
    def __delete_unused_models(cls, user):
        cls.objects.filter(user=user, order_model=None).delete()

    def save(self, *args, **kwargs):
        self.amount_integer = calculate_amount_integer(amount=self.amount)
        self.__delete_unused_models(self.user)
        super().save(*args, **kwargs)


class OrderModel(models.Model):
    order_calc = models.OneToOneField(
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
            send_date = tz.now() + timedelta(days=1)
            delete_order_from_actives.apply_async((self.pk,), eta=send_date)

        if self.filtering and self.sending:
            self.send_messages_speed = self.__get_send_messages_speed_per_minutes()
            self.sending_start_at = tz.now()

        return super().save(*args, **kwargs)

    @property
    def time_from_sending_start_at(self):
        return int((tz.now() - self.sending_start_at).total_seconds())

    def __get_send_messages_speed_per_minutes(self):
        amount = int(self.order_calc.amount[:-1])
        seconds_ago = int((self.sending_end_at -
                           tz.now()).total_seconds())

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
            if self.sending_end_at <= tz.now() and not self.sending:
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
    discount = models.IntegerField(
        validators=[MaxValueValidator(100), MinValueValidator(1)])
    uses = models.IntegerField(default=0)
    number_of_uses = models.IntegerField(default=1)
    user = models.ManyToManyField(
        get_user_model(), related_name='coupon', null=True, blank=True)

    @property
    def left_to_use(self):
        return self.number_of_uses

    def get_discount_modifier(self) -> float:
        return (100 - self.discount) / 100

    def __str__(self):
        return f'{self.name}, number_of_uses = {self.number_of_uses}'
