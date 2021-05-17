from django.urls import path
from . import views

urlpatterns = [
    path('model',views.make_model),
    path('',views.sensor_data),
]
