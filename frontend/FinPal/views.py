from django.shortcuts import render

def chat(request):
    return render(request, 'chat.html')

def chat2_view(request):
    return render(request, 'chat2.html')
