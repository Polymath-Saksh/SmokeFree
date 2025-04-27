from django.shortcuts import render, redirect 
from .models import Team

def dashboard(request):
    user_teams = Team.objects.all()  # Fetch all teams from the database
    return render(request, 'teams/dashboard.html', {'teams': user_teams})  

def create_team(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            team = Team.objects.create(name=name)
            team.members.add(request.user)
            return redirect('teams:dashboard')
    return render(request, 'teams/create_team.html')

# Create your views here.
