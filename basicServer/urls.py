from django.urls import path
from . import views

urlpatterns = [
    path('check',views.sensor_data),
]
