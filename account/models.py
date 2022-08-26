from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    receive_news = models.BooleanField(default=True)
    receive_activity = models.BooleanField(default=True)