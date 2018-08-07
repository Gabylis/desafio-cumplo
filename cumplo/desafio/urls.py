from django.urls import path, include
from . import views

urlpatterns = [
    path('home',views.home),
    path('get-data',views.get_data),
    path('get-chart-data',views.get_chart_data),
]
