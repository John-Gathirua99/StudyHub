# views.py
from django.http import JsonResponse

def chatbot_response(request):
    if request.method == "POST":
        user_message = request.POST.get('message')
        
        # Simple logic OR connect to OpenAI/Rasa here
        if "hello" in user_message.lower():
            bot_reply = "Hi there! How can I help you today?"
        else:
            bot_reply = "Sorry, I didn’t understand that."

        return JsonResponse({'reply': bot_reply})
