from django.urls import path
from . import views

app_name = 'cravings'

urlpatterns = [
    path('log/', views.log_craving, name='log_craving'),
]