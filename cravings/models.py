from django.db import models
from django.conf import settings

class CravingLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cravings')
    timestamp = models.DateTimeField(auto_now_add=True)
    intensity = models.IntegerField(default=1) #Scale 1-5
    trigger = models.CharField(max_length=255, blank=True, null=True) #What triggered the craving
    notes = models.TextField(blank=True, null=True) #Additional notes about the craving
    location = models.CharField(max_length=255, blank=True, null=True) #Where the craving occurred
    duration = models.IntegerField(default=0) #Duration of the craving in minutes

    def __str__(self):
        return f"{self.user.username} - {self.timestamp} - Intensity: {self.intensity}"
    
    def get_user(self):
        return self.user.username
    
    def get_intensity(self):
        return self.intensity

    def get_trigger(self):
        return self.trigger
    
    def get_location(self):
        return self.location
    
    def get_duration(self):
        return self.duration
    
    def get_notes(self):
        return self.notes
    
    def get_timestamp(self):
        return self.timestamp.strftime("%Y-%m-%d %H:%M:%S")
    
    def get_craving_data(self):
        return {
            'user': self.get_user(),
            'intensity': self.get_intensity(),
            'trigger': self.get_trigger(),
            'location': self.get_location(),
            'duration': self.get_duration(),
            'notes': self.get_notes(),
            'timestamp': self.get_timestamp()
        }
    
    def get_summary(self):
        return f"Craving by {self.get_user()} with intensity {self.get_intensity()} at {self.get_timestamp()}."

# Create your models here.
