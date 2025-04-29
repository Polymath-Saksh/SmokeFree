# cravings/forms.py
from django import forms
from .models import CravingLog

class CravingLogForm(forms.ModelForm):
    class Meta:
        model = CravingLog
        fields = ['intensity', 'trigger', 'notes', 'latitude', 'longitude','duration']
        widgets = {
            'latitude': forms.HiddenInput(),
            'longitude': forms.HiddenInput(),
            'duration': forms.NumberInput(attrs={
                'min': 0,
                'class': 'form-control'
            }),
            'intensity': forms.NumberInput(attrs={
                'min': 1,
                'max': 5,
                'class': 'form-control'
            }),
            'trigger': forms.TextInput(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        labels = {
            'intensity': 'Craving Intensity (1-5)',
            'trigger': 'What triggered this craving?',
            'duration': 'Duration of Craving (in minutes)',
            'notes': 'Additional Notes'
        }
