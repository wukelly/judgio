from django.shortcuts import render

from .models import Judge

def home(request):
    # check if user is checked in judge
    if request.user.is_authenticated:
        judge = Judge.objects.filter(user_id = request.user.id)
        if len(judge) and judge[0].checked_in:
                return render(request, 'home.html', {'name': judge[0].name(), 'checked_in': True})
    return render(request, 'home.html', {'checked_in': False})