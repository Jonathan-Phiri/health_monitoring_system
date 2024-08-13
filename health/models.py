from django.db import models

# Create your models here.
class Temperature(models.Model):
    data = models.CharField(max_length=20)

class Heartrate(models.Model):
    data = models.CharField(max_length=20)

class Bloodpressure(models.Model):
    data = models.CharField(max_length=20)