from django.shortcuts import render
from .models import Notification

def notification_list(request):
    notifications = Notification.objects.filter(
        user=request.user).order_by('-created_at')
    return render(request,
                   'notifications/list.html',
                   {'notifications': notifications})

# Create your views here.
