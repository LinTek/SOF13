from django.contrib.auth.views import login as auth_login

from django.shortcuts import render, redirect


from .models import Shift


def login(request, **kwargs):
    if request.user.is_authenticated():
        return redirect('shifts')
    else:
        return auth_login(request, **kwargs)


def shifts(request):
    s = Shift.objects.all()

    return render(request, 'functionary/shifts.html', {'shifts': s})
