from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Renders chat page
def chat(request):
    return render(request, 'chat.html')

# Chatbot endpoint
@csrf_exempt
@api_view(['POST'])
def chat_with_bot(request):
    user_message = request.data.get('message')

    if not user_message:
        return Response({"error": "No message provided"}, status=400)

    try:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful financial advisor."},
                {"role": "user", "content": user_message}
            ]
        )
        bot_response = completion.choices[0].message.content
        return Response({"botResponse": bot_response})

    except Exception as e:
        return Response({"error": f"Internal server error: {str(e)}"}, status=500)
