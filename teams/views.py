from django.shortcuts import render, redirect, get_object_or_404
from .models import Team
from django.contrib import messages

def dashboard(request):
    user_teams = request.user.teams.all()  # Fetch only teams the logged-in user is a member of
    return render(request, 'teams/dashboard.html', {'teams': user_teams})

def create_team(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            team = Team.objects.create(name=name)
            team.members.add(request.user)
            return redirect('teams:dashboard')
    return render(request, 'teams/create_team.html')

def join_team(request):
    if request.method == 'POST':
        code = request.POST.get('access_code', '').upper()
        try:
            team = Team.objects.get(access_code=code)
            team.members.add(request.user)
            messages.success(request, f'You have successfully joined the team "{team.name}".')
            return redirect('teams:dashboard')
        except Team.DoesNotExist:
            messages.error(request, 'Invalid access code. Please try again.')
    return render(request, 'teams/join_team.html')

def team_cravings(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    # Ensure only team members can view
    if request.user not in team.members.all():
        return render(request, 'teams/not_authorized.html')
    cravings = team.get_all_cravings()
    return render(request, 'teams/team_cravings.html', {'team': team, 'cravings': cravings})