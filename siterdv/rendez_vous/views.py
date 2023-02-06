from django.shortcuts import render

# Create your views here.


def home (request):
    return (request, 'rendez_vous/index.html')

def login(request):
    return (request, 'rendez_vous/login.html')

def logout(request):
    return (request, 'rendez_vous/logout.html')

def register(request):
    return(request, 'rendez_vous/register.html')

