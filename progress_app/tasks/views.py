from django.shortcuts import render

def index(request):
    return render(request, 'tasks/index.html')

def game(request):
    return render(request, 'tasks/game.html')
