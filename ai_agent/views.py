# ai_agent/views.py
import os
from django.shortcuts import render
from django.http import StreamingHttpResponse
from django.contrib.auth.decorators import login_required
from azure.ai.inference import ChatCompletionsClient
from azure.core.credentials import AzureKeyCredential
from cravings.models import CravingLog

@login_required
def ai_chat(request):
    if request.method == 'GET':
        return render(request, 'ai_agent/chat.html')
        
    def event_stream():
        endpoint = os.getenv("AZURE_ENDPOINT")
        api_key = os.getenv("AZURE_API_KEY")

        # Add user context using get_last_craving
        username = request.user.username
        name = request.user.name if hasattr(request.user, 'name') else username
        gender = request.user.gender if hasattr(request.user,'gender') else 'N/A'
        age = request.user.age if hasattr(request.user, 'age') else 'N/A'

        last_craving = CravingLog.objects.filter(user=request.user).order_by('-timestamp').first()
        if last_craving:
            last = last_craving.get_last_craving()
            craving_context = (
                f"User's last craving: "
                f"Intensity {last.intensity}, "
                f"Trigger: {last.trigger or 'N/A'}, "
                f"Notes: {last.notes or 'N/A'}, "
                f"Time: {last.timestamp.strftime('%Y-%m-%d %H:%M:%S')}."
            )
        else:
            craving_context = "No craving logs found for this user."

        system_message = (
            "You are a supportive smoking cessation coach providing empathetic, practical advice. Start with displaying a friendly, personalised greeting to the user and the last craving context. "
            f"User context: name is {name}, gender {gender}, age {age}."
        )

        client = ChatCompletionsClient(
            endpoint=endpoint,
            credential=AzureKeyCredential(api_key)
        )
        
        try:
            response = client.complete(
                stream=True,
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": request.POST.get('message', '')}
                ],
                max_tokens=4096,
                temperature=0.7,
                model="gpt-4o-mini"  # Use your actual deployment name
            )
            
            for chunk in response:
                if chunk.choices and chunk.choices[0].delta.content:
                    yield f"data: {chunk.choices[0].delta.content}\n\n"
        finally:
            client.close()
            
    return StreamingHttpResponse(event_stream(), content_type="text/event-stream")
