# insights/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from cravings.models import CravingLog
from django.db import models
from datetime import datetime, timedelta
import pandas as pd
from azure.ai.inference import ChatCompletionsClient
from azure.core.credentials import AzureKeyCredential
import os
from dotenv import load_dotenv
import json

load_dotenv()

@login_required
def personal_dashboard(request):
    user = request.user
    cravings = CravingLog.objects.filter(user=user).order_by('-timestamp')
    
    # Basic stats
    stats = {
        'total_cravings': cravings.count(),
        'avg_intensity': cravings.aggregate(models.Avg('intensity'))['intensity__avg'],
        'days_since_start': (datetime.now().date() - user.date_joined.date()).days
    }
    
    # Time pattern analysis
    df = pd.DataFrame(list(cravings.values('timestamp', 'intensity', 'trigger')))
    if not df.empty:
        df['hour'] = pd.to_datetime(df['timestamp']).dt.hour
        time_patterns = df['hour'].value_counts().head(3).to_dict()
        stats['common_times'] = {f"{k}:00": v for k, v in time_patterns.items()}
    
    # Prepare map data
    map_data = [{
        'lat': float(c.latitude),
        'lng': float(c.longitude),
        'info': f"{c.timestamp.strftime('%Y-%m-%d')}<br>Intensity: {c.intensity}/5"
    } for c in cravings if c.latitude and c.longitude]
    
    # Get AI suggestions
    suggestions = generate_ai_suggestions(user)
    
    return render(request, 'insights/dashboard.html', {
        'stats': stats,
        'map_data': map_data,  # Pass as Python list, not as JSON string
        'suggestions': suggestions,
        'google_maps_api_key': os.getenv("GOOGLE_MAPS_API_KEY")
    })

def generate_ai_suggestions(user):
    """Use Azure AI to analyze user's data"""
    client = ChatCompletionsClient(
        endpoint=os.getenv("AZURE_ENDPOINT"),
        credential=AzureKeyCredential(os.getenv("AZURE_API_KEY"))
    )
    
    cravings_data = "\n".join([
        f"{c.timestamp}: {c.trigger} (Intensity {c.intensity})" 
        for c in CravingLog.objects.filter(user=user)
    ])
    
    response = client.complete(
        model=os.environ.get("AZURE_MODEL_NAME", "gpt-4o-mini"),
        messages=[{
            "role": "system",
            "content": f"Analyze this user's craving patterns and suggest 3 actionable strategies: {cravings_data}"
        }]
    )
    
    return [s.strip() for s in response.choices[0].message.content.split("\n") if s.strip()]
