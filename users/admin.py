from django.contrib import admin
from .models import CustomUser
# Register your models here.
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'name', 'gender', 'age', 'email', 'phone_number', 'is_staff', 'is_active')
    search_fields = ('username', 'email', 'name')
    list_filter = ('gender', 'is_staff', 'is_active')