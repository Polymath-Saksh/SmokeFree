from django.urls import path
from . import views

app_name = 'teams'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('create/', views.create_team, name='create_team'),
    path('<int:team_id>/cravings/', views.team_cravings, name='team_cravings'),
    path('join/', views.join_team, name='join_team'),
]