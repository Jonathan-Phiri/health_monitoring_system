from django.db import models
from django.utils import timezone

class Temperature(models.Model):
    data = models.FloatField()
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Temperature: {self.data}°C at {self.timestamp}"

    class Meta:
        ordering = ['-timestamp']

class HeartRate(models.Model):
    data = models.FloatField()
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Heart Rate: {self.data} BPM at {self.timestamp}"

    class Meta:
        ordering = ['-timestamp']