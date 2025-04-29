# users/utils.py
import random
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone

def generate_otp():
    return str(random.randint(100000, 999999))

def send_otp_email(email, otp):
    send_mail(
        subject="Your Password Reset OTP",
        message=f"Your OTP for password reset is: {otp}. It is valid for 10 minutes.",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        fail_silently=False,
    )
