from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    # You can use first_name and last_name from AbstractUser, or add a 'name' field if you want a single field
    name = models.CharField(max_length=150, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(unique=True, blank=True, null=True)

    reset_otp = models.CharField(max_length=6, blank=True, null=True, default=None)
    reset_otp_created = models.DateTimeField(blank=True, null=True, default=None)
    
    def __str__(self):
        return self.username
    def get_full_name(self):
        # Prefer 'name' if filled, else fallback to first/last name
        if self.name:
            return self.name
        elif self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.username
    def get_gender_display(self):
        return self.gender
    def get_age(self):
        return self.age if self.age else "Age not provided"
    def get_short_name(self):
        return self.first_name if self.first_name else self.username
    def get_phone_number(self):
        return self.phone_number if self.phone_number else "No phone number provided"
    def get_email(self):
        return self.email if self.email else "No email provided"
    
    
# Create your models here.
