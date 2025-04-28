from django.urls import path
from . import views

app_name = 'ai_agent'

urlpatterns = [
    path('chat/', views.ai_chat, name='chat'),
]
