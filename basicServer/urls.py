from django.urls import path
from . import views

urlpatterns = [
    path('model',views.make_model),
    path('result',views.result_data),
    path('save', views.save_data)
]
