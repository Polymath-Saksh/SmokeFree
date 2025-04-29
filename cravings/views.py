# cravings/views.py
from django.shortcuts import render, redirect
from .models import CravingLog
from .forms import CravingLogForm  # We'll create this form next

def log_craving(request):
    if request.method == 'POST':
        form = CravingLogForm(request.POST)
        if form.is_valid():
            craving = form.save(commit=False)
            craving.user = request.user
            craving.save()
            return redirect('teams:dashboard')
    else:
        # Initialize form with empty location data
        form = CravingLogForm(initial={
            'latitude': 0.0,
            'longitude': 0.0
        })
    return render(request, 'cravings/log_craving.html', {'form': form})
