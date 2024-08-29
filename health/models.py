from django.db import models

# Create your models here.
class Temperature(models.Model):
    data = models.CharField(max_length=20)

