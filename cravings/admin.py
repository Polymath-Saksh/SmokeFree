from django.contrib import admin
from .models import CravingLog

@admin.register(CravingLog)
class CravingLogAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'timestamp',
        'intensity',
        'trigger',
        'location',
        'duration',
        'notes',
    )
    list_filter = ('intensity', 'trigger', 'location', 'timestamp')
    search_fields = ('trigger', 'notes', 'location')

    