# encoding: utf-8
from itertools import groupby

from django.conf import settings
from django.contrib.auth.views import login as auth_login
from django.http import HttpResponse

from django.shortcuts import render, redirect

from .models import Shift, WorkerRegistration
from .forms import NewFunctionaryForm, AddFunctionaryForm
from .kobra_client import KOBRAClient


def _group_by_type(lst):
    return [(key, list(shifts)) for key, shifts in groupby(lst, key=lambda shift: shift.shift_type)]


def login(request, **kwargs):
    if request.user.is_authenticated():
        return redirect('shifts')
    else:
        return auth_login(request, **kwargs)


def shifts(request):
    registrations = WorkerRegistration.objects.filter(worker=request.user)
    all_shifts = _group_by_type(list(
                        Shift.objects.order_by('shift_type', 'start')))
    return render(request, 'functionary/shifts.html', {
                                        'registrations': registrations,
                                        'all_shifts': all_shifts})


def add_worker(request):
    WorkerRegistration(shift_id=int(request.POST.get('shift')),
                       worker=request.user).save()

    return HttpResponse('ok')


def search(request):
    form = NewFunctionaryForm(request.POST or None)
    error = None

    if form.is_valid():
        k = KOBRAClient(settings.KOBRA_USER, settings.KOBRA_KEY)
        liu_id = form.cleaned_data.get('liu_id')
        student = None

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
            error = 'Blocked user or LiU-card'

    return render(request, 'functionary/search.html',
                    {'form': form, 'error': error})
