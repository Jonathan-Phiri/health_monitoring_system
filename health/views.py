from django.shortcuts import render
from rest_framework import generics
from .models import Temperature
from .serializer import TemperatureSerializer
from rest_framework.views import APIView
from rest_framework.response import Response

class MonitorDetailView(generics.RetrieveAPIView):
    queryset = Temperature.objects.all()
    serializer_class = TemperatureSerializer


class MonitorListView(generics.ListAPIView):
    queryset = Temperature.objects.all()
    serializer_class = TemperatureSerializer


class MonitorCreateAPIView(generics.CreateAPIView):
    queryset = Temperature.objects.all()
    serializer_class = TemperatureSerializer


class LatestTemperatureAPIView(APIView):
    def get(self, request):
        # Retrieve the latest temperature based on the timestamp field
        latest_temperature = Temperature.objects.latest('timestamp')
        return Response({"temperature": latest_temperature.data})
    
def monitor(request):
    return render(request, 'monitor.html')
