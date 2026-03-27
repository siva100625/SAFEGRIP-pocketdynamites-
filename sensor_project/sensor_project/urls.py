from django.urls import path, include
from rest_framework.routers import DefaultRouter
from sensor_data.views import SensorDataViewSet
from django.contrib import admin


urlpatterns = [

    path('api/auth/',include('sensor_data.urls')),

]
