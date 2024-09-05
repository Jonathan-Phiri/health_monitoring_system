from django.urls import path
from .views import MonitorDetailView,  MonitorListView, LatestTemperatureAPIView, MonitorCreateAPIView, monitor,history_view

urlpatterns = [
    path('temperatures/', MonitorListView.as_view(), name='temperature-list'),
    path('temperatures/<int:pk>/', MonitorDetailView.as_view(), name='temperature-detail'),
    path('createtemperatures/', MonitorCreateAPIView.as_view(), name='temperature-create'),
    path('api/latest-temperature/', LatestTemperatureAPIView.as_view(), name='latest-temperature'),
    path('monitor/', monitor, name='monitor'),
    path('history/', history_view, name='history'),
]

