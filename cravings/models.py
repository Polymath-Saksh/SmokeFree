# cravings/models.py

from django.db import models
from django.conf import settings

class CravingLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cravings')
    timestamp = models.DateTimeField(auto_now_add=True)
    intensity = models.IntegerField(default=1)
    trigger = models.CharField(max_length=255, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    duration = models.IntegerField(default=0)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)

    def get_last_craving(self):
        return CravingLog.objects.filter(user=self.user).order_by('-timestamp').first()
    def __str__(self):
        return f"{self.user.username} - {self.timestamp} - Intensity: {self.intensity}"
