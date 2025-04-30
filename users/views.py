from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.decorators import login_required
from .forms import UserProfileForm, ForgotPasswordForm, OTPVerifyForm
from django.contrib import messages
from .models import CustomUser
from django.utils import timezone
from datetime import timedelta

from .utils import generate_otp, send_otp_email
class CustomUserCreationForm(UserCreationForm):

    name = forms.CharField(max_length=150, required=False, label="Full Name")
    gender = forms.ChoiceField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], required=False)
    age = forms.IntegerField(required=False, min_value=0)
    email = forms.EmailField(required=True, label="Email")  # <-- Add this line

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + ('name','gender','age','email')  # <-- Add 'email'

    def save(self, commit=True):
        user = super().save(commit=False)
        user.name = self.cleaned_data['name']
        user.gender = self.cleaned_data['gender']
        user.age = self.cleaned_data['age']
        user.email = self.cleaned_data['email']  # <-- Save email
        if commit:
            user.save()
        return user

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('teams:dashboard')  # Redirect to a success page or home page
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile was updated successfully!')
            return redirect('users:profile')
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, 'users/profile.html', {'form': form})

def forgot_password(request):
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = CustomUser.objects.get(email=email)
                otp = generate_otp()
                user.reset_otp = otp
                user.reset_otp_created = timezone.now()
                user.save()
                send_otp_email(email, otp)
                messages.success(request, "OTP sent to your email.")
                return redirect('users:verify_otp')  # URL name for OTP verification page
            except CustomUser.DoesNotExist:
                messages.error(request, "No user with that email.")
    else:
        form = ForgotPasswordForm()
    return render(request, 'users/forgot_password.html', {'form': form})

def verify_otp(request):
    if request.method == 'POST':
        form = OTPVerifyForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            otp = form.cleaned_data['otp']
            new_password = form.cleaned_data['new_password']
            try:
                user = CustomUser.objects.get(email=email)
                # Check OTP and expiry (10 min)
                if (user.reset_otp == otp and 
                    user.reset_otp_created and 
                    timezone.now() - user.reset_otp_created < timedelta(minutes=10)):
                    user.set_password(new_password)
                    user.reset_otp = None
                    user.reset_otp_created = None
                    user.save()
                    messages.success(request, "Password reset successful. You can now log in.")
                    return redirect('login')
                else:
                    messages.error(request, "Invalid or expired OTP.")
            except CustomUser.DoesNotExist:
                messages.error(request, "Invalid email.")
    else:
        # Pre-fill email if passed as GET param
        form = OTPVerifyForm(initial={'email': request.GET.get('email', '')})
    return render(request, 'users/verify_otp.html', {'form': form})

def homepage(request):
    if not request.user.is_authenticated:
        return redirect('login')  # Replace 'login' with your login url name
    return render(request, 'homepage.html')