from django.contrib.postgres.fields import ArrayField
from django.contrib.auth import get_user_model
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
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
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
    order_calc = models.ForeignKey(OrderCalcModel, on_delete=models.CASCADE)

    targets_or_competitors_submited = models.TextField(
        max_length=100_000)
    use_our_default_filtering = models.BooleanField()
    not_use_any_filtering = models.BooleanField()
    message = models.TextField(max_length=1000)
    attach_in_message = models.TextField(max_length=600)
    additional_information = models.TextField(max_length=600)
    contact_details = models.CharField(max_length=1000)

    def __str__(self):
        return f'{self.order_calc}'
