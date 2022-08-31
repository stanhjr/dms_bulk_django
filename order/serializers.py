from rest_framework import serializers

from . import models


class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BoardModel
        fields = '__all__'
