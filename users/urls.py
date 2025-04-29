from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path("register/", views.register, name="register"),
    path("profile/", views.profile, name="profile"),
    path("forgot_password/", views.forgot_password, name="forgot_password"),
    path("verify_otp/", views.verify_otp, name="verify_otp"),
]