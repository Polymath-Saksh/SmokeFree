# insights/urls.py
from django.urls import path
from . import views

app_name = 'insights'
urlpatterns = [
    path('dashboard/', views.personal_dashboard, name='dashboard'),
]
