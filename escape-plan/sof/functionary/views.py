from django.conf import settings
from django.contrib.auth.views import login as auth_login

from django.shortcuts import render, redirect

from .models import Shift
from .forms import NewFunctionaryForm
from .kobra_client import KOBRAClient


def login(request, **kwargs):
    if request.user.is_authenticated():
        return redirect('shifts')
    else:
        return auth_login(request, **kwargs)


def shifts(request):
    s = Shift.objects.all()

    return render(request, 'functionary/shifts.html', {'shifts': s})


def register(request):
    form = NewFunctionaryForm(request.POST or None)

    if form.is_valid():
        k = KOBRAClient(settings.KOBRA_USER, settings.KOBRA_KEY)
        liu_id = form.cleaned_data.get('liu_id')
        student = None

        if liu_id:
            student = k.get_student_by_liu_id(liu_id)

        else:
            card_number = form.cleaned_data.get('liu_card_number')

            if card_number:
                student = k.get_student_by_card(card_number)

        if student:
            return render(request, 'functionary/add_functionary.html')

    return render(request, 'functionary/register.html', {'form': form})
