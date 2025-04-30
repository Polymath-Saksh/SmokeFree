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
    
    # Get AI insights and strategies
    insights, strategies = generate_ai_insights_and_strategies(user)

    return render(request, 'insights/dashboard.html', {
        'stats': stats,
        'map_data': map_data,
        'insights': insights,
        'strategies': strategies,
        'google_maps_api_key': os.getenv("GOOGLE_MAPS_API_KEY")
    })

def generate_ai_insights_and_strategies(user):
    """Use Azure AI to analyze user's data and extract insights and actionable strategies as lists"""
    client = ChatCompletionsClient(
        endpoint=os.getenv("AZURE_ENDPOINT"),
        credential=AzureKeyCredential(os.getenv("AZURE_API_KEY"))
    )

    cravings_data = "\n".join([
        f"{c.timestamp}: {c.trigger} (Intensity {c.intensity})"
        for c in CravingLog.objects.filter(user=user)
    ])

    prompt = (
        "Analyze this user's craving patterns and provide:\n"
        "1. Three concise insights about their craving behavior.\n"
        "2. Three actionable strategies to help them manage cravings.\n"
        "Format:\n"
        "Insights:\n"
        "1. ...\n"
        "2. ...\n"
        "3. ...\n"
        "Strategies:\n"
        "1. ...\n"
        "2. ...\n"
        "3. ...\n"
        f"User data:\n{cravings_data}"
    )

    response = client.complete(
        model=os.environ.get("AZURE_MODEL_NAME", "gpt-4o-mini"),
        messages=[{
            "role": "system",
            "content": prompt
        }]
    )

    content = response.choices[0].message.content

    # Parse insights and strategies from the response
    insights, strategies = [], []
    section = None
    for line in content.splitlines():
        line = line.strip()
        if line.lower().startswith("insights"):
            section = "insights"
            continue
        if line.lower().startswith("strategies"):
            section = "strategies"
            continue
        if section and line and line[0] in "123" and line[1] == ".":
            text = line[2:].strip()
            # Remove markdown bold (**)
            text = text.replace("**", "")
            if section == "insights" and len(insights) < 3:
                insights.append(text)
            elif section == "strategies" and len(strategies) < 3:
                strategies.append(text)
        if len(insights) == 3 and len(strategies) == 3:
            break

    # Fallback: if parsing fails, show the whole content as a single item
    if not insights:
        insights = [content]
    if not strategies:
        strategies = [content]

    # Split each strategy into (title, rest) at the first colon for template rendering
    def split_title_rest(text):
        text = text.strip()
        if not text:
            return ("", "")
        if ':' in text:
            idx = text.find(':')
            title = text[:idx]
            rest = text[idx+1:].lstrip()
            return (title, rest)
        else:
            return (text, "")

    strategies = [split_title_rest(s) for s in strategies]

    return insights, strategies
