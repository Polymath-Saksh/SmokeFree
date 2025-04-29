# insights/models.py
from django.db import models
from django.conf import settings

class UserInsight(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    last_updated = models.DateTimeField(auto_now=True)
    top_triggers = models.JSONField(default=list)
    common_locations = models.JSONField(default=list)
    time_patterns = models.JSONField(default=list)
