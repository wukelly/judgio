from django.shortcuts import render

from .models import Judge

def home(request):
    # check if user is checked in judge
    if request.user.is_authenticated:
        judge = Judge.objects.filter(user_id = request.user.id)
        if len(judge):
            judge = judge[0]
            name = judge.name()
            return render(request, 'home.html', {'name': name, 'judge': True})

    return render(request, 'home.html', {'judge': False})