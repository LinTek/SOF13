# encoding: utf-8
import json
from itertools import groupby

from django.db import transaction
from django.conf import settings
from django.contrib.auth.views import login as auth_login
from django.contrib.auth.decorators import login_required, permission_required

from django.http import HttpResponse, Http404
from django.utils.translation import ugettext_lazy as _
from django.template.loader import render_to_string
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
    all_shifts = _group_by_type(list(Shift.objects.with_free_places(worker=request.user)))

    return render(request, 'functionary/shifts.html', {
                                        'registrations': registrations,
                                        'all_shifts': all_shifts})


@login_required
@permission_required('auth.add_user')
@transaction.commit_on_success
def add_registration(request):
    try:
        worker = Worker.objects.get(pk=int(request.POST.get('worker')))
        shift = Shift.objects.select_for_update().get(pk=int(request.POST.get('shift')))

    except Shift.DoesNotExist, Worker.DoesNotExist:
        raise Http404

    try:
        worker_registration = shift.workerregistration_set.get(worker_id=worker.pk)
        worker_registration.delete()
        response = {'book_status': 'deleted'}

    except WorkerRegistration.DoesNotExist:
        if shift.workerregistration_set.count() >= shift.max_workers:
            response = {'book_status': 'occupied'}
            return HttpResponse(json.dumps(response), content_type="application/json")

        WorkerRegistration(shift=shift,
                           worker=worker).save()
        response = {'book_status': 'ok'}

    shift.free_places = shift.max_workers - shift.workerregistration_set.count()
    html = render_to_string('functionary/partials/shift_title.html',
                            {'shift': shift, 'place_count': True})
    response['html'] = html
    return HttpResponse(json.dumps(response),
                        content_type="application/json")


@login_required
@permission_required('auth.add_user')
def create_worker(request):
    form = AddWorkerForm(request.POST)

    if form.is_valid():
        worker = form.save(commit=False)
        worker.username = worker.email
        worker.save()
        return redirect('add_registrations', worker_id=worker.pk)

    return render(request, 'functionary/add_functionary.html', {'form': form})


@login_required
@permission_required('auth.add_user')
def add_registrations(request, worker_id):
    worker = get_object_or_404(Worker, pk=worker_id)
    all_shifts = _group_by_type(list(Shift.objects.with_free_places(worker)))

    return render(request, 'functionary/add_registrations.html',
                            {'worker': worker, 'all_shifts': all_shifts})


@login_required
@permission_required('auth.add_user')
def search(request):
    def render_worker_form(initial={}):
        form = AddWorkerForm(initial=initial)
        return render(request, 'functionary/add_functionary.html', {'form': form})

    form = SearchForm(request.POST or None)
    error = None

    if form.is_valid():
        k = KOBRAClient(settings.KOBRA_USER, settings.KOBRA_KEY)
        term = form.cleaned_data.get('term')

        if not term:
            return render_worker_form()

        try:
            student = k.get_student(term)

            if student.get('blocked'):
                error = _('Blocked user or LiU-card')

            else:
                return render_worker_form({
                    'first_name': student.get('first_name').title(),
                    'last_name': student.get('last_name').title(),
                    'email': student.get('email'),
                    'lintek': student.get('union') == 'LinTek',
                    'pid': student.get('personal_number'),
                })

        except StudentNotFound:
            error = _('Student was not found')

        except ValueError:
            error = _('Could not get the result')

    return render(request, 'functionary/search.html',
                    {'form': form, 'error': error})
