from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from .models import Temperature, HeartRate
from .serializer import TemperatureSerializer, HeartRateSerializer

# Temperature Views
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
            latest_heartrate = HeartRate.objects.latest('timestamp')
            return Response({
                "temperature": latest_temperature.data,
                "heart_rate": latest_heartrate.data if latest_heartrate else None,
                "temperature_timestamp": latest_temperature.timestamp,
                "heart_rate_timestamp": latest_heartrate.timestamp if latest_heartrate else None
            })
        except Temperature.DoesNotExist:
            return Response(
                {"error": "No temperature data available."}, 
                status=status.HTTP_404_NOT_FOUND
            )

# Heart Rate Views
class HeartRateDetailView(generics.RetrieveAPIView):
    queryset = HeartRate.objects.all()
    serializer_class = HeartRateSerializer

class HeartRateListView(generics.ListAPIView):
    queryset = HeartRate.objects.all()
    serializer_class = HeartRateSerializer

class HeartRateCreateAPIView(generics.CreateAPIView):
    queryset = HeartRate.objects.all()
    serializer_class = HeartRateSerializer

class LatestHeartRateAPIView(APIView):
    def get(self, request):
        try:
            latest_heartrate = HeartRate.objects.latest('timestamp')
            return Response({"heart_rate": latest_heartrate.data})
        except HeartRate.DoesNotExist:
            return Response(
                {"error": "No heart rate data available."}, 
                status=status.HTTP_404_NOT_FOUND
            )

# Combined Data Views
class LatestVitalsAPIView(APIView):
    def get(self, request):
        try:
            latest_temperature = Temperature.objects.latest('timestamp')
            latest_heartrate = HeartRate.objects.latest('timestamp')
            
            return Response({
                "temperature": {
                    "value": latest_temperature.data,
                    "timestamp": latest_temperature.timestamp
                },
                "heart_rate": {
                    "value": latest_heartrate.data,
                    "timestamp": latest_heartrate.timestamp
                }
            })
        except (Temperature.DoesNotExist, HeartRate.DoesNotExist) as e:
            return Response(
                {"error": "Some vital signs data is missing."}, 
                status=status.HTTP_404_NOT_FOUND
            )

# Template Views
def monitor(request):
    return render(request, 'monitor.html')

def vitals_history(request):
    temperature_data = Temperature.objects.all().order_by('-timestamp')
    heartrate_data = HeartRate.objects.all().order_by('-timestamp')
    
    context = {
        'temperature_data': temperature_data,
        'heartrate_data': heartrate_data
    }
    return render(request, 'history.html', context)

# Combined Create View for ESP32 Data
class VitalsCreateAPIView(APIView):
    def post(self, request):
        try:
            data = request.data
            
            # Create temperature record if temperature data is present
            if 'temperature' in data:
                temp_serializer = TemperatureSerializer(data={'data': data['temperature']})
                if temp_serializer.is_valid():
                    temp_serializer.save()
            
            # Create heart rate record if heart rate data is present
            if 'heart_rate' in data:
                hr_serializer = HeartRateSerializer(data={'data': data['heart_rate']})
                if hr_serializer.is_valid():
                    hr_serializer.save()
            
            return Response({
                "message": "Vitals data recorded successfully"
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response({
                "error": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)