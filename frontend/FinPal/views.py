from django.shortcuts import render

def chat(request):
    return render(request, 'chat.html')

def home_view(request):
    return render(request, 'home.html')
