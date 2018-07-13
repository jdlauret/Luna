from django.shortcuts import render, redirect

def index(request):
    return render(request, 'global.html')

def agent(request):
    return render (request, 'agent_view.html')

def transaction(request):
    return render (request, 'transaction_window.html')