from django.shortcuts import render, redirect
from .models import CravingLog

def log_craving(request):
    if request.method == 'POST':
        intensity = int(request.POST.get('intensity',1))
        trigger = request.POST.get('trigger','')
        notes = request.POST.get('notes','')
        CravingLog.objects.create(
            user=request.user,
            intensity=intensity,
            trigger=trigger,
            notes=notes
        )
        return redirect('teams:dashboard')  # Redirect to a success page or home page
    return render(request, 'cravings/log_craving.html')
# Create your views here.
