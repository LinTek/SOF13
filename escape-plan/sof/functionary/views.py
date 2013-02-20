from django.conf import settings
from django.contrib.auth.views import login as auth_login

from django.shortcuts import render, redirect

from .models import Shift
from .forms import NewFunctionaryForm, AddFunctionaryForm
from .kobra_client import KOBRAClient


def login(request, **kwargs):
    if request.user.is_authenticated():
        return redirect('shifts')
    else:
        return auth_login(request, **kwargs)


def shifts(request):
    s = Shift.objects.all()

    return render(request, 'functionary/shifts.html', {'shifts': s})


def search(request):
    form = NewFunctionaryForm(request.POST or None)

    if form.is_valid():
        k = KOBRAClient(settings.KOBRA_USER, settings.KOBRA_KEY)
        liu_id = form.cleaned_data.get('liu_id')
        student = None
        is_blocked = False

        # TODO: Move all user and KOBRA-stuff to some other place...
        if liu_id:
            student = k.get_student_by_liu_id(liu_id)

        else:
            card_number = form.cleaned_data.get('liu_card_number')

            if card_number:
                student = k.get_student_by_card(card_number)

        if student:
            if not student.get('blocked'):
                form = AddFunctionaryForm(initial={
                    'first_name': student.get('first_name'),
                    'last_name': student.get('last_name'),
                    'liu_id': student.get('liu_id'),
                    'email': student.get('email'),
                })
                return render(request, 'functionary/add_functionary.html', {'form': form})
            is_blocked = True

    return render(request, 'functionary/search.html',
                    {'form': form, 'is_blocked': is_blocked})
