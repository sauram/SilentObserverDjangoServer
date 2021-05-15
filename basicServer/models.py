from django.db import models
from django.db.models.fields import CharField
from django.db.models.fields.json import JSONField

class SensorData(models.Model):
    userId = models.CharField(max_length=50)
    values = JSONField()

    def __str__(self) -> str:
        return super().__str__()
