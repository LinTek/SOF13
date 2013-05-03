# encoding: utf-8
import json
import datetime
from itertools import groupby

from django.db import transaction
from django.db.models import Count
from django.conf import settings
from django.contrib.auth.views import login as auth_login
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse, Http404
from django.utils.translation import ugettext_lazy as _
from django.template.loader import render_to_string
from django.shortcuts import render, redirect, get_object_or_404

from sof.utils.kobra_client import KOBRAClient, StudentNotFound

from .models import Shift, WorkerRegistration, Worker, ShiftType
from .forms import SearchForm, AddWorkerForm


def _group_by_type(lst):
    return [(key, list(shifts)) for key, shifts in groupby(lst, key=lambda shift: shift.shift_type)]


def _group_by_shift(lst):
    return [(key, list(regs)) for key, regs in groupby(lst, key=lambda r: r.shift)]


def login(request, **kwargs):
    if request.user.is_authenticated():
        return redirect('shifts')
    else:
        return auth_login(request, **kwargs)


def public_shift_list(request):
    all_shifts = _group_by_type(list(Shift.objects.with_free_places()))

    return render(request, 'functionary/public_shift_list.html',
                  {'all_shifts': all_shifts})


@login_required
def shifts(request):
    registrations = WorkerRegistration.objects.filter(worker=request.user)
    all_shifts = _group_by_type(list(Shift.objects.with_free_places(worker=request.user)))

    return render(request, 'logged_in.html',
                  {'registrations': registrations,
                   'all_shifts': all_shifts})


@login_required
@permission_required('auth.add_user')
@transaction.commit_on_success
def add_registration(request):
    try:
        worker = Worker.objects.get(pk=int(request.POST.get('worker') or 0))
        shift = Shift.objects.select_for_update().get(pk=int(request.POST.get('shift') or 0))

    except (Shift.DoesNotExist, Worker.DoesNotExist):
        raise Http404

    try:
        worker_registration = shift.workerregistration_set.get(worker_id=worker.pk)
        worker_registration.delete()
        response = {'book_status': 'deleted'}

    except WorkerRegistration.DoesNotExist:
        if shift.workerregistration_set.count() >= shift.max_workers:
            response = {'book_status': 'occupied'}

        else:
            wr = WorkerRegistration(shift=shift,
                                    worker=worker)
            wr.save()
            response = {'book_status': 'ok'}

    shift.free_places = max(0, shift.max_workers - shift.workerregistration_set.count())
    html = render_to_string('functionary/partials/shift_title.html',
                            {'shift': shift, 'place_count': True, 'admin': True})
    response['html'] = html
    return HttpResponse(json.dumps(response),
                        content_type="application/json")


@login_required
@permission_required('auth.add_user')
def approve_contract(request, worker_id):
    worker = get_object_or_404(Worker, pk=worker_id)
    worker.contract_approved = True
    worker.save()

    return redirect('add_registrations', worker_id=worker_id)


@login_required
@permission_required('auth.add_user')
def create_worker(request):
    form = AddWorkerForm(request.POST)

    if form.is_valid():
        worker = form.save(commit=False)
        worker.lintek_member = form.cleaned_data.get('lintek', False)
        worker.save()
        return redirect('add_registrations', worker_id=worker.pk)

    return render(request, 'functionary/add_functionary.html', {'form': form})


@login_required
@permission_required('auth.add_user')
def list_workers(request):
    workers = (Worker.objects.order_by('first_name', 'last_name')
               .annotate(wcount=Count('workerregistration'))
               .filter(wcount__gt=0))

    no_contract = workers.filter(contract_approved=False)
    no_meta_info = workers.filter(has_meta_info=False)

    return render(request, 'functionary/list.html',
                  {'workers': workers, 'no_contract': no_contract,
                   'no_meta_info': no_meta_info})


@login_required
@permission_required('auth.add_user')
def workers_by_type(request):
    shift_types = ShiftType.objects.order_by('name')

    for shift_type in shift_types:
        regs = (WorkerRegistration.objects
                .filter(shift__shift_type=shift_type)
                .select_related('worker')
                .order_by('worker__first_name', 'worker__last_name'))
        seen = set()
        shift_type.workers = [r.worker for r in regs if not r.worker in seen and not seen.add(r.worker)]

    return render(request, 'functionary/list_by_type.html',
                  {'shift_types': shift_types})


@login_required
@permission_required('auth.add_user')
def worker_check_in(request, date=None):
    dates = sorted(set(s.start.date() for s in Shift.objects.all()))

    if date:
        try:
            date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
        except ValueError:
            raise Http404

        if not date in dates:
            raise Http404

    registrations = (WorkerRegistration.objects
                     .select_related('worker', 'shift', 'shift__shift_type',
                                     'shift__shift_sub_type')
                     .order_by('shift__start', 'shift__end', 'shift__id'))

    if date:
        registrations = registrations.filter(shift__start__day=date.day, shift__start__month=date.month, shift__start__year=date.year)

    shifts = _group_by_shift(list(registrations))

    for shift, regs in shifts:
        regs.sort(key=lambda r: (r.worker.first_name, r.worker.last_name))

    return render(request, 'functionary/worker_check_in.html',
                  {'shifts': shifts, 'dates': dates})


@login_required
@permission_required('auth.add_user')
def toggle_checked_in(request):
    r = get_object_or_404(WorkerRegistration, pk=request.POST.get('registration', 0))
    r.checked_in = (not r.checked_in)

    if r.checked_out:
        r.checked_out = False

    r.save()
    return render(request, 'functionary/partials/check_in_status.html', {'r': r})


@login_required
@permission_required('auth.add_user')
def toggle_checked_out(request):
    r = get_object_or_404(WorkerRegistration, pk=request.POST.get('registration', 0))
    r.checked_out = (not r.checked_out)
    r.save()
    return render(request, 'functionary/partials/check_in_status.html', {'r': r})


@login_required
@permission_required('auth.add_user')
def add_registrations(request, worker_id):
    worker = get_object_or_404(Worker, pk=worker_id)
    all_shifts = _group_by_type(list(Shift.objects.with_free_places(worker)))
    worker_shifts = worker.workerregistration_set.select_related('shift')

    return render(request, 'functionary/add_registrations.html',
                  {'worker': worker,
                   'all_shifts': all_shifts,
                   'worker_shifts': worker_shifts})


@login_required
@permission_required('auth.add_user')
def send_confirmation(request, worker_id):
    worker = get_object_or_404(Worker, pk=worker_id)
    worker.send_registration_email()

    if not worker.welcome_email_sent:
        worker.send_welcome_email()

        worker.welcome_email_sent = True
        worker.save()

    return redirect('search')


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
            w = Worker.objects.search(term)
            return redirect('add_registrations', worker_id=w.pk)

        except Worker.DoesNotExist:
            pass

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
