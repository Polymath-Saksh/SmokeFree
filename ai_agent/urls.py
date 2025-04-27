from django.urls import path
from . import views

app_name = 'ai_agent'

urlpatterns = [
    path('motivation/', views.get_motivational_quote, name='get_motivation'),
]
