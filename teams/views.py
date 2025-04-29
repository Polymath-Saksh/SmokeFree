from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Team
from cravings.models import CravingLog  # Added import
from azure.ai.inference import ChatCompletionsClient
from azure.core.credentials import AzureKeyCredential
import os
from datetime import datetime, timezone
from .utils import generate_team_stats  # Import the function to generate team stats

@login_required
def dashboard(request):
    user_teams = request.user.teams.all()
    
    try:
        quote = get_gpt_quote()
    except Exception as e:
        # Fallback to default quotes if API fails
        default_quotes = [
            "Every craving resisted is a victory!",
            "You're stronger than your cravings!",
            "One day at a time - you've got this!"
        ]
        import random
        quote = random.choice(default_quotes)
    
    time_since_last = get_time_since_last_craving(request.user)
    
    return render(request, 'teams/dashboard.html', {
        'teams': user_teams,
        'quote': quote,
        'time_since_last': time_since_last
    })

@login_required
def create_team(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            team = Team.objects.create(name=name)
            team.members.add(request.user)
            return redirect('teams:dashboard')
    return render(request, 'teams/create_team.html')

@login_required
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

@login_required
def team_cravings(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    if request.user not in team.members.all():
        return render(request, 'teams/not_authorized.html')
    
    cravings = team.get_all_cravings().order_by('-timestamp')[:5]  # Show latest 5 by timestamp
    stats, chart = generate_team_stats(team)
    
    context = {
        'team': team,
        'cravings': cravings,
        'stats': stats,
        'compliance_chart': chart
    }
    return render(request, 'teams/team_cravings.html', context)

def get_gpt_quote():
    """Get motivational quote from GPT-4o-mini"""
    client = ChatCompletionsClient(
        endpoint=os.getenv("AZURE_ENDPOINT"),
        credential=AzureKeyCredential(os.getenv("AZURE_API_KEY"))
    )
    
    try:
        response = client.complete(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a motivational coach for people trying to quit smoking."},
                {"role": "user", "content": "Generate a one-line motivational quote. Max 10 words."}
            ],
            max_tokens=32,
            temperature=0.7,
            stream=False
        )
        
        quote = ""
        for choice in response.choices:
            if choice.message.content:
                quote += choice.message.content.strip('"')
        return quote
    
    finally:
        client.close()

def get_time_since_last_craving(user):
    """Calculate time since user's last craving"""
    last_craving = CravingLog.objects.filter(user=user).order_by('-timestamp').first()
    
    if not last_craving:
        return "No cravings logged yet! 🎉"
    
    now = datetime.now(timezone.utc)
    delta = now - last_craving.timestamp
    
    days = delta.days
    hours, remainder = divmod(delta.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    
    time_parts = []
    if days > 0:
        time_parts.append(f"{days} day{'s' if days > 1 else ''}")
    if hours > 0:
        time_parts.append(f"{hours} hour{'s' if hours > 1 else ''}")
    if minutes > 0:
        time_parts.append(f"{minutes} minute{'s' if minutes > 1 else ''}")
    
    if not time_parts:
        return "Just now!"
    
    return "Last craving: " + ", ".join(time_parts) + " ago 💪"
