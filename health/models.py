from django.db import models

class Temperature(models.Model):
    data = models.CharField(max_length=20)
    timestamp = models.DateTimeField(auto_now_add=True)  


