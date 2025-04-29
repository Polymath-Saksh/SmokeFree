from django.shortcuts import render, redirect
from .models import CravingLog
from .forms import CravingLogForm
from teams.models import Team  # Import Team model
from .utils import send_craving_notification  # Import email utility
import os
import requests
from django.utils import timezone
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.environ.get("GOOGLE_MAPS_API_KEY")
def log_craving(request):
    if request.method == 'POST':
        form = CravingLogForm(request.POST)
        if form.is_valid():
            craving = form.save(commit=False)
            craving.user = request.user
            
            # Get coordinates from form
            lat = form.cleaned_data['latitude']
            lng = form.cleaned_data['longitude']
            
            # Reverse geocode using Google API
            if lat and lng:
                url = f"https://maps.googleapis.com/maps/api/geocode/json?latlng={lat},{lng}&key={API_KEY}"
                
                try:
                    response = requests.get(url).json()
                    if response['results']:
                        # Extract formatted address
                        craving.location = response['results'][0]['formatted_address']
                except Exception as e:
                    # Handle API errors gracefully
                    pass
            
            craving.save()
            return redirect('teams:dashboard')
    else:
        form = CravingLogForm()
    return render(request, 'cravings/log_craving.html', {
        'form': form,
        'google_maps_api_key': API_KEY,})

