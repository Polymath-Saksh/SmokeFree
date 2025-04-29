from django.contrib import admin
from .models import Team

@admin.register(Team)
class TeamsAdmin(admin.ModelAdmin):
    list_display = ('name', 'display_members', 'created_at', 'updated_at', 'access_code')
    search_fields = ('name', 'access_code')
    list_filter = ('created_at', 'updated_at')
    ordering = ('-created_at',)
    
    def display_members(self, obj):
        """Display team members as a comma-separated string"""
        return ", ".join([member.username for member in obj.members.all()[:3]])
    
    display_members.short_description = 'Members'  # Column header in admin
    display_members.admin_order_field = 'members'