from django.db import models


class FAQModel(models.Model):
    question = models.CharField(max_length=90)
    answer = models.TextField(max_length=1000)
