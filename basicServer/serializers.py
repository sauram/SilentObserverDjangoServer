from django.db.models import fields
from rest_framework import serializers
from . import models

class SensorDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SensorData
        fields=['userId','values']
