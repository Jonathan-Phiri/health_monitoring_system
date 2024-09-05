from django.shortcuts import render
from rest_framework import generics
from .models import Temperature
from .serializer import TemperatureSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime

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
        try:
            latest_temperature = Temperature.objects.latest('timestamp')
            return Response({"temperature": latest_temperature.data})
        except Temperature.DoesNotExist:
            return Response({"error": "No temperature data available."}, status=status.HTTP_404_NOT_FOUND)
    
def monitor(request):
    return render(request, 'monitor.html')

def temperature_history(request):
    temperature_data = Temperature.objects.all().order_by('-timestamp')  # Fetch all temperature data, ordered by timestamp
    return render(request, 'history.html', {'temperature_data': temperature_data})


