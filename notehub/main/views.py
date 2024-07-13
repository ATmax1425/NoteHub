from django.shortcuts import render

def index(request):
    return render(request, 'main/index.html')

def login(request):
    pass

def register(request):
    pass