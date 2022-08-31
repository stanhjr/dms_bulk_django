from rest_framework import serializers

from . import models


class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Board
        fields = '__all__'
