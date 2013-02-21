# encoding: utf-8
from itertools import groupby

from django.conf import settings
from django.contrib.auth.views import login as auth_login
from django.http import HttpResponse

from django.shortcuts import render, redirect

from .models import Shift, WorkerRegistration
from .forms import SearchForm, AddWorkerForm
from .kobra_client import KOBRAClient, StudentNotFound


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
    def next(initial={}):
        form = AddWorkerForm(initial=initial)
        return render(request, 'functionary/add_functionary.html', {'form': form})

    form = SearchForm(request.POST or None)
    error = None

    if form.is_valid():
        k = KOBRAClient(settings.KOBRA_USER, settings.KOBRA_KEY)
        term = form.cleaned_data.get('term')

        if not term:
            return next()

        try:
            student = k.get_student(term)

            if student.get('blocked'):
                error = 'Blocked user or LiU-card'

            else:
                return next({
                    'first_name': student.get('first_name').title(),
                    'last_name': student.get('last_name').title(),
                    'liu_id': student.get('liu_id'),
                    'email': student.get('email'),
                    'lintek': student.get('union') == 'LinTek'
                })

        except StudentNotFound:
            error = 'Student was not found!'

    return render(request, 'functionary/search.html',
                    {'form': form, 'error': error})
