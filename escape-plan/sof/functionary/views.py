# encoding: utf-8
from itertools import groupby

from django.conf import settings
from django.contrib.auth.views import login as auth_login
from django.contrib.auth.decorators import login_required, permission_required

from django.http import HttpResponse
from django.utils.translation import ugettext_lazy as _

from django.shortcuts import render, redirect, get_object_or_404

from .models import Shift, WorkerRegistration, Worker
from .forms import SearchForm, AddWorkerForm
from .kobra_client import KOBRAClient, StudentNotFound


def _group_by_type(lst):
    return [(key, list(shifts)) for key, shifts in groupby(lst, key=lambda shift: shift.shift_type)]


def login(request, **kwargs):
    if request.user.is_authenticated():
        return redirect('shifts')
    else:
        return auth_login(request, **kwargs)


@login_required
def shifts(request):
    registrations = WorkerRegistration.objects.filter(worker=request.user)
    all_shifts = _group_by_type(list(Shift.objects.with_free_places()))

    return render(request, 'functionary/shifts.html', {
                                        'registrations': registrations,
                                        'all_shifts': all_shifts})


@login_required
@permission_required('auth.add_user')
def add_worker(request):
    shift = get_object_or_404(Shift, pk=int(request.POST.get('shift')))

    if shift.workerregistration_set.count() >= shift.max_workers:
        return HttpResponse('occupied')

    WorkerRegistration(shift=shift,
                       worker=request.user).save()

    return HttpResponse('ok')


@login_required
@permission_required('auth.add_user')
def register_worker(request):
    form = AddWorkerForm(request.POST)

    if form.is_valid():
        worker = form.save(commit=False)
        worker.username = worker.liu_id
        worker.save()

        return redirect('add_registrations', worker_id=worker.pk)
    return render(request, 'functionary/add_functionary.html', {'form': form})


@login_required
@permission_required('auth.add_user')
def add_registrations(request, worker_id):
    worker = get_object_or_404(Worker, pk=worker_id)
    all_shifts = _group_by_type(list(Shift.objects.with_free_places()))

    return render(request, 'functionary/add_registrations.html',
                            {'worker': worker, 'all_shifts': all_shifts})


@login_required
@permission_required('auth.add_user')
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
                error = _('Blocked user or LiU-card')

            else:
                return next({
                    'first_name': student.get('first_name').title(),
                    'last_name': student.get('last_name').title(),
                    'liu_id': student.get('liu_id'),
                    'email': student.get('email'),
                    'lintek': student.get('union') == 'LinTek'
                })

        except StudentNotFound:
            error = _('Student was not found')

        except ValueError:
            error = _('Could not get the result')

    return render(request, 'functionary/search.html',
                    {'form': form, 'error': error})
