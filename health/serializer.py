from rest_framework import serializers
from .models import Temperature, Heartrate, Bloodpressure

class TemperatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Temperature
        fields = ['data']

class HeartrateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Heartrate
        fields = ['data']

class BloodpressureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bloodpressure
        fields = ['data']
