from django.contrib.postgres.fields import ArrayField
from django.db import models


class Board(models.Model):
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
