from django.shortcuts import render
from rest_framework import generics
from .models import Temperature, Heartrate, Bloodpressure
from .serializer import TemperatureSerializer, HeartrateSerializer, BloodpressureSerializer
from rest_framework.views import APIView
from rest_framework.response import Response

class MonitorDetailView(generics.RetrieveAPIView):
    queryset = Temperature.objects.all()
    serializer_class = TemperatureSerializer

    queryset = Heartrate.objects.all()
    serializer_class = HeartrateSerializer

    queryset = Bloodpressure.objects.all()
    serializer_class = BloodpressureSerializer


class MonitorListView(generics.ListAPIView):
    queryset = Temperature.objects.all()
    serializer_class = TemperatureSerializer

    queryset = Heartrate.objects.all()
    serializer_class = HeartrateSerializer

    queryset = Bloodpressure.objects.all()
    serializer_class = BloodpressureSerializer


class MonitorCreateAPIView(generics.CreateAPIView):
    queryset = Temperature.objects.all()
    serializer_class = TemperatureSerializer

    queryset = Heartrate.objects.all()
    serializer_class = HeartrateSerializer

    queryset = Bloodpressure.objects.all()
    serializer_class = BloodpressureSerializer

class LatestTemperatureAPIView(APIView):
    def get(self, request):
        latest_temperature = Temperature.objects.latest('id')
        return Response({"temperature": latest_temperature.data})
    
def monitor(request):
    return render(request, 'monitor.html')
