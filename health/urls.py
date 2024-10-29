from django.urls import path
from . import views

urlpatterns = [
    path('monitor/', views.monitor, name='monitor'),
    path('history/', views.vitals_history, name='vitals_history'),
    
    # Temperature endpoints
    path('api/temperature/', views.MonitorListView.as_view(), name='temperature-list'),
    path('api/temperature/<int:pk>/', views.MonitorDetailView.as_view(), name='temperature-detail'),
    path('api/temperature/create/', views.MonitorCreateAPIView.as_view(), name='temperature-create'),
    path('api/temperature/latest/', views.LatestTemperatureAPIView.as_view(), name='temperature-latest'),
    
    # Heart rate endpoints
    path('api/heartrate/', views.HeartRateListView.as_view(), name='heartrate-list'),
    path('api/heartrate/<int:pk>/', views.HeartRateDetailView.as_view(), name='heartrate-detail'),
    path('api/heartrate/create/', views.HeartRateCreateAPIView.as_view(), name='heartrate-create'),
    path('api/heartrate/latest/', views.LatestHeartRateAPIView.as_view(), name='heartrate-latest'),
    
    # Combined endpoints
    path('api/vitals/latest/', views.LatestVitalsAPIView.as_view(), name='vitals-latest'),
    path('api/vitals/create/', views.VitalsCreateAPIView.as_view(), name='vitals-create'),
]