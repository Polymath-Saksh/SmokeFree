from django.shortcuts import render, redirect
from .models import CravingLog
from .forms import CravingLogForm
from teams.models import Team  # Import Team model
from .utils import send_craving_notification  # Import email utility
import os
from django.utils import timezone
from dotenv import load_dotenv

load_dotenv()
def log_craving(request):
    if request.method == 'POST':
        form = CravingLogForm(request.POST)
        if form.is_valid():
            # Save craving with user and location data
            craving = form.save(commit=False)
            craving.user = request.user
            craving.timestamp = timezone.now()
            craving.save()

            # Get all teams the user belongs to
            user_teams = Team.objects.filter(members=request.user)
            print("User Teams:")
            print(user_teams)  # Debugging line to check user teams
            print("Views Address",os.environ.get("AZURE_EMAIL_CONNECTION_STRING"))
            # sender = os.environ.get("AZURE_SENDER_ADDRESS")
            # Collect all unique team members' emails (excluding current user)
            recipients = set()
            for team in user_teams:
                for member in team.members.exclude(id=request.user.id):
                    if member.email:  # Only add users with verified emails
                        recipients.add(member.email)
            print("Recipients:")
            print(recipients)
            # print(f"Sender: {sender}")
            
            # Send notifications if there are recipients
            if recipients:
                send_craving_notification(craving, list(recipients))

            return redirect('teams:dashboard')
    else:
        # Initialize form with default location data
        form = CravingLogForm(initial={
            'latitude': 0.0,
            'longitude': 0.0
        })
    
    return render(request, 'cravings/log_craving.html', {
        'form': form,
        'google_maps_api_key': os.environ.get("GOOGLE_MAPS_API_KEY"),})

