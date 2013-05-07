# encoding: utf-8
import json
import datetime

from django.db import transaction
from django.db.models import Count, Q
from django.conf import settings
from django.core.exceptions import MultipleObjectsReturned
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.translation import ugettext_lazy as _
from django.template.loader import render_to_string
from django.template import RequestContext
from django.middleware.csrf import get_token

from sof.utils.forms import format_pid
from sof.utils.kobra_client import (KOBRAClient, StudentNotFound, get_kwargs)
from sof.functionary.models import Person, Visitor, Worker
from sof.invoices.models import Invoice

from .models import Ticket, TicketType
from .forms import (TicketTypeForm, TurboTicketForm, VisitorForm, SearchForm,
                    LiuIDForm, PreemptionTicketTypeForm, WorkerForm, PublicTicketTypeForm)


class InvoiceExists():
    pass


class TicketSoldOut():
    pass


@login_required
@permission_required('tickets.add_ticket')
@transaction.commit_on_success
def turbo_confirm(request):
    response = {}
    ticket_type_form = TicketTypeForm(request.POST, display_all=request.user.is_staff)

    worker_id = request.GET.get('worker_id')
    visitor_id = request.GET.get('visitor_id')
    if worker_id:
        worker_id = int(worker_id)
        worker_form = WorkerForm(request.POST,
                                 instance=Person.objects.get(pk=worker_id))

    elif visitor_id:
        worker_form = WorkerForm()
        visitor_id = int(visitor_id)
        visitor_form = VisitorForm(request.POST,
                                   instance=Person.objects.get(pk=visitor_id))

    else:
        worker_form = WorkerForm()
        visitor_form = VisitorForm(request.POST)

    if ticket_type_form.is_valid():
        ticket_type_ids = ticket_type_form.cleaned_data.get('ticket_type')

        if (worker_id and worker_form.is_valid()) or visitor_form.is_valid():
            if worker_form.is_valid():
                person = worker_form.save()
            else:
                person = visitor_form.save()

            if ticket_type_ids:
                invoice = create_invoice(person)

                for ticket_type_id in ticket_type_ids:
                    ticket = Ticket.objects.create(ticket_type_id=ticket_type_id,
                                                   invoice=invoice,
                                                   person=person)
                    ticket.send_as_email()
                invoice.send_as_email()

            response['is_valid'] = True
            return HttpResponse(json.dumps(response),
                                content_type='application/json')

    response['is_valid'] = False
    return HttpResponse(json.dumps(response),
                        content_type='application/json')


@login_required
@permission_required('tickets.add_ticket')
@transaction.commit_on_success
def turbo_submit(request):
    response = {}
    worker_job_count = None
    worker_no_contract = False
    error = None
    ticket_type_form = TicketTypeForm(request.POST or None, display_all=request.user.is_staff)
    turbo_form = TurboTicketForm(request.POST or None)

    csrf_token_value = get_token(request)

    if turbo_form.is_valid() and ticket_type_form.is_valid():
        client = KOBRAClient(settings.KOBRA_USER, settings.KOBRA_KEY)
        term = turbo_form.cleaned_data.get('term')
        ticket_type_ids = ticket_type_form.cleaned_data.get('ticket_type')

        try:
            for ticket_type_id in ticket_type_ids:
                ticket_type = TicketType.objects.select_for_update().get(pk=ticket_type_id)

                if ticket_type.ticket_set.count() >= ticket_type.max_amount:
                    raise TicketSoldOut()

            try:
                # The person already exists, it may be a Worker or a "double-blipp"
                person = Person.objects.search(term)

                # However, it must not have an invoice yet for this form
                if Invoice.objects.filter(person=person).exists():
                    raise InvoiceExists()

                try:
                    person.worker
                    person_form = WorkerForm(instance=person)
                    response['worker_id'] = person.id
                    worker_job_count = person.worker.workerregistration_set.count()
                    worker_no_contract = not person.worker.contract_approved

                except Worker.DoesNotExist:
                    person_form = VisitorForm(instance=person)
                    response['visitor_id'] = person.id

            except Person.DoesNotExist:
                # Otherwise, fetch the person from KOBRA
                student = client.get_student(term)
                person_form = VisitorForm(instance=Visitor(**get_kwargs(student)))

            response['is_valid'] = True
            response['html'] = render_to_string('tickets/partials/turbo_confirm.html',
                                                {'ticket_type_form': ticket_type_form,
                                                 'person_form': person_form,
                                                 'worker_job_count': worker_job_count,
                                                 'worker_no_contract': worker_no_contract,
                                                 'csrf_token_value': csrf_token_value},
                                                RequestContext(request))
            return HttpResponse(json.dumps(response),
                                content_type='application/json')

        except TicketSoldOut:
            error = _('This ticket type is sold out')

        except StudentNotFound:
            error = _('Student was not found')

        except InvoiceExists:
            error = _('An invoice already exist for this person')

        except ValueError:
            error = _('Could not get the result')

    response['is_valid'] = False
    response['html'] = render_to_string('tickets/partials/turbo.html',
                                        {'ticket_type_form': ticket_type_form,
                                         'turbo_form': turbo_form,
                                         'error': error}, RequestContext(request))

    return HttpResponse(json.dumps(response),
                        content_type='application/json')


@login_required
@permission_required('tickets.add_ticket')
@transaction.commit_on_success
def sell(request):
    error = None
    person = None

    ticket_type_form = TicketTypeForm(request.POST or None, display_all=request.user.is_staff)
    visitor_form = VisitorForm(request.POST or None)
    search_form = SearchForm(request.POST or None)

    tickets = (Ticket.objects
               .select_related('ticket_type', 'invoice', 'invoice__person')
               .filter(invoice__is_verified=True)
               .order_by('-sell_date')[:10])

    if request.user.is_staff:
        stats = TicketType.objects.all().annotate(sold=Count('ticket'))
    else:
        stats = TicketType.objects.active().annotate(sold=Count('ticket'))

    if visitor_form.is_valid() and ticket_type_form.is_valid():
        visitor = visitor_form.save(commit=False)
        visitor.save()

        ticket_type_ids = ticket_type_form.cleaned_data.get('ticket_type')

        if ticket_type_ids:
            invoice = create_invoice(visitor)

            for ticket_type_id in ticket_type_ids:
                ticket = Ticket.objects.create(ticket_type_id=ticket_type_id,
                                               invoice=invoice,
                                               person=visitor)
                ticket.send_as_email()
            invoice.send_as_email()

        return redirect('ticket_sell')

    elif search_form.is_valid():
        try:
            tickets = None
            q = search_form.cleaned_data.get('q')

            if q.isdigit():
                tickets = Ticket.objects.filter(pk=int(q))

            if tickets:
                person = tickets[0].person
            else:
                try:
                    person = Person.objects.search(q)

                except Person.DoesNotExist:
                    if ' ' in q and len(q.split()) == 2:
                        first, last = q.split()
                        person = Person.objects.get(first_name__istartswith=first,
                                                    last_name__istartswith=last)
                    else:
                        person = Person.objects.get(Q(first_name__istartswith=q) |
                                                    Q(last_name__istartswith=q))

            return redirect('person_details', pk=person.pk)

        except Person.DoesNotExist:
            error = _('The person was not found')

        except Person.MultipleObjectsReturned:
            error = _('More than one object matched the query')

    return render(request, 'tickets/sell.html',
                  {'ticket_type_form': ticket_type_form,
                   'turbo_form': TurboTicketForm(),
                   'visitor_form': visitor_form,
                   'search_form': search_form,
                   'latest_tickets': tickets,
                   'ticket_stats': stats,
                   'error': error})


@login_required
@permission_required('tickets.add_ticket')
def person_details(request, pk):
    person = get_object_or_404(Person, pk=pk)
    try:
        person = person.worker
    except Worker.DoesNotExist:
        person = person.visitor

    error = new_person = None
    move_form = LiuIDForm(request.POST or None)

    if move_form.is_valid():
        try:
            new_person = Person.objects.search(move_form.cleaned_data.get('liu_id'))
            invoice = person.invoice_set.get()

            for ticket in invoice.ticket_set.all():
                ticket.person = new_person
                ticket.save()

                ticket.send_as_email()

        except Person.DoesNotExist:
            error = _('The person was not found')

        except MultipleObjectsReturned:
            error = _('The current invoice holder has multiple invoices and someone was too lazy to implement support for that')

    tickets = person.ticket_set.filter(invoice__is_verified=True)
    tickets_handed_out = all([t.is_handed_out for t in tickets])

    invoices = person.invoice_set.all()
    special_invoices = person.specialinvoice_set.all()

    return render(request, 'tickets/person_details.html',
                  {'person': person,
                   'tickets': tickets,
                   'tickets_handed_out': tickets_handed_out,
                   'invoices': invoices,
                   'special_invoices': special_invoices,
                   'move_form': move_form, 'error': error,
                   'new_person': new_person})


@transaction.commit_on_success
def public_sell(request):
    error = ''
    success = False
    liu_id_form = LiuIDForm(request.POST or None)
    ticket_type_form = PublicTicketTypeForm(request.POST or None)

    if liu_id_form.is_valid() and ticket_type_form.is_valid():
        try:
            term = liu_id_form.cleaned_data['liu_id']

            try:
                person = Person.objects.search(term=term)

                if person.invoice_set.exists():
                    raise InvoiceExists()

            except Person.DoesNotExist:
                client = KOBRAClient(settings.KOBRA_USER, settings.KOBRA_KEY)
                student = client.get_student(term)
                visitor = Visitor.objects.create(**get_kwargs(student))
                person = visitor.person_ptr

            invoice = Invoice(person=person, is_verified=False)
            invoice.generate_data()
            invoice.save()

            ticket_type_ids = ticket_type_form.cleaned_data.get('ticket_type')

            for ticket_type_id in ticket_type_ids:
                ticket_type = TicketType.objects.select_for_update().get(pk=ticket_type_id)

                if ticket_type.ticket_set.count() >= ticket_type.max_amount:
                    raise TicketSoldOut()

                Ticket.objects.create(invoice=invoice, ticket_type=ticket_type, person=person)
            invoice.send_verify_email()

            success = True
            liu_id_form = LiuIDForm()
            ticket_type_form = PublicTicketTypeForm()

        except TicketSoldOut:
            error = _('This ticket type is sold out')

        except InvoiceExists:
            error = _('An invoice already exist for this person')

        except StudentNotFound:
            error = _('Student was not found')

    return render(request, 'tickets/public_sell.html',
                  {'ticket_type_form': ticket_type_form,
                   'liu_id_form': liu_id_form,
                   'error': error, 'success': success})


@transaction.commit_on_success
def preemption(request):
    error = ''
    success = False
    liu_id_form = LiuIDForm(request.POST or None)
    ticket_type_form = PreemptionTicketTypeForm(request.POST or None)

    if liu_id_form.is_valid() and ticket_type_form.is_valid():
        try:
            try:
                worker = Worker.objects.select_for_update().get(liu_id=liu_id_form.cleaned_data.get('liu_id'))
            except Worker.DoesNotExist:
                pid = format_pid(liu_id_form.cleaned_data.get('liu_id'))
                if pid:
                    worker = Worker.objects.select_for_update().get(pid=pid)
                else:
                    raise Worker.DoesNotExist

            if worker.invoice_set.exists():
                raise InvoiceExists()

            person = worker.person_ptr
            invoice = Invoice(person=person, is_verified=False)
            invoice.generate_data()
            invoice.send_verify_email()
            invoice.save()

            ticket_type_ids = ticket_type_form.cleaned_data.get('ticket_type')

            for ticket_type_id in ticket_type_ids:
                Ticket.objects.create(invoice=invoice,
                                      ticket_type_id=ticket_type_id,
                                      person=person)

            success = True
            liu_id_form = LiuIDForm()
            ticket_type_form = PreemptionTicketTypeForm()

        except Worker.DoesNotExist:
            error = _('The functionary was not found')

        except InvoiceExists:
            error = _('An invoice already exist for this person')

    return render(request, 'tickets/preemption.html',
                  {'ticket_type_form': ticket_type_form,
                   'liu_id_form': liu_id_form,
                   'error': error, 'success': success})


def confirm(request, token):
    invoice = get_object_or_404(Invoice, token=token)

    if not invoice.is_verified:
        invoice.is_verified = True

        # For people which confirms old invoices
        if invoice.due_date < datetime.date.today() + datetime.timedelta(days=7):
            invoice.due_date = datetime.date.today() + datetime.timedelta(days=7)
        invoice.save()

        for ticket in invoice.ticket_set.all():
            ticket.send_as_email()
        invoice.send_as_email()

    return render(request, 'tickets/confirm.html')


def create_invoice(person):
    invoice = Invoice(person=person, is_verified=True)
    invoice.generate_data()
    invoice.save()
    return invoice
