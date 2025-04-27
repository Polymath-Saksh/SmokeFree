from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    
    def __str__(self):
        return self.username
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}" if self.first_name and self.last_name else self.username
    def get_short_name(self):
        return self.first_name if self.first_name else self.username
    def get_phone_number(self):
        return self.phone_number if self.phone_number else "No phone number provided"
    def get_email(self):
        return self.email if self.email else "No email provided"
    
    
# Create your models here.
