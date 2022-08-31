from django.contrib.postgres.fields import ArrayField
from django.contrib.auth import get_user_model
from django.db import models


class BoardModel(models.Model):
    instagram_board_quantity = ArrayField(
        models.FloatField(), size=13)
    instagram_board_amount = ArrayField(models.IntegerField(), size=13)
    instagram_board_discount = ArrayField(models.IntegerField(), size=13)

    twitter_board_quantity = ArrayField(
        models.FloatField(), size=13)
    twitter_board_amount = ArrayField(models.IntegerField(), size=13)
    twitter_board_discount = ArrayField(models.IntegerField(), size=13)

    discord_board_quantity = ArrayField(
        models.FloatField(), size=13)
    discord_board_amount = ArrayField(models.IntegerField(), size=13)
    discord_board_discount = ArrayField(models.IntegerField(), size=13)

    telegram_board_quantity = ArrayField(
        models.FloatField(), size=13)
    telegram_board_amount = ArrayField(models.IntegerField(), size=13)
    telegram_board_discount = ArrayField(models.IntegerField(), size=13)


SOCIAL_NETWORK_CHOICES = (
    ('1', 'instagram'),
    ('2', 'twitter'),
    ('3', 'discord'),
    ('4', 'telegram')
)


class OrderModel(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    social_network = models.CharField(
        max_length=9, choices=SOCIAL_NETWORK_CHOICES)

    targets_or_competitors_submited = models.TextField(
        blank=True, max_length=100_000)
    use_our_default_filtering = models.BooleanField(blank=True)
    not_use_any_filtering = models.BooleanField(blank=True)
    message = models.TextField(blank=True, max_length=1000)
    attach_in_message = models.TextField(blank=True, max_length=600)
    additional_information = models.TextField(blank=True, max_length=600)
    contact_details = models.CharField(blank=True, max_length=1000)
