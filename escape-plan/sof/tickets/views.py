# encoding: utf-8
from django.db import transaction
from django.db.models import Count
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.translation import ugettext_lazy as _

from sof.utils.kobra_client import (KOBRAClient, StudentNotFound, get_kwargs)
from sof.functionary.models import Person, Visitor, Worker
from sof.invoices.models import Invoice

from .models import Ticket, TicketType
from .forms import (TicketTypeForm, TurboTicketForm, VisitorForm, SearchForm,
                    LiuIDForm, PreemptionTicketTypeForm)


class InvoiceExists():
    pass


class TicketSoldOut():
    pass


@login_required
@permission_required('tickets.add_ticket')
@transaction.commit_on_success
def sell(request):
    error = None
    person = None

    ticket_type_form = TicketTypeForm(request.POST or None)
    turbo_form = TurboTicketForm(request.POST or None)
    visitor_form = VisitorForm(request.POST or None)
    search_form = SearchForm(request.GET or None)

    tickets = Ticket.objects.select_related('ticket_type', 'invoice', 'invoice__person').order_by('-sell_date')[:10]

    stats = TicketType.objects.active().annotate(sold=Count('ticket'))

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

            except Person.DoesNotExist:
                # Otherwise, fetch the person from KOBRA
                student = client.get_student(term)

                person = Visitor(**get_kwargs(student))
                person.save()

            invoice = create_invoice(person)

            for ticket_type_id in ticket_type_ids:
                Ticket.objects.create(ticket_type_id=ticket_type_id, invoice=invoice)

            return redirect('ticket_sell')

        except TicketSoldOut:
            error = _('This ticket type is sold out')

        except StudentNotFound:
            error = _('Student was not found')

        except InvoiceExists:
            error = _('An invoice already exist for this person')

        except ValueError:
            error = _('Could not get the result')

    elif visitor_form.is_valid() and ticket_type_form.is_valid():
        visitor = visitor_form.save(commit=False)
        visitor.save()

        invoice = create_invoice(visitor)

        for ticket_type_id in ticket_type_form.cleaned_data.get('ticket_type'):
            Ticket.objects.create(ticket_type_id=ticket_type_id,
                                  invoice=invoice)

        return redirect('ticket_sell')

    elif search_form.is_valid():
        try:
            person = Person.objects.search(search_form.cleaned_data.get('q'))
            return redirect('person_details', pk=person.pk)

        except Person.DoesNotExist:
            error = _('The person was not found')

    return render(request, 'tickets/sell.html',
                  {'ticket_type_form': ticket_type_form,
                   'turbo_form': turbo_form,
                   'visitor_form': visitor_form,
                   'search_form': search_form,
                   'latest_tickets': tickets,
                   'ticket_stats': stats,
                   'error': error})


@login_required
@permission_required('tickets.add_ticket')
def person_details(request, pk):
    person = get_object_or_404(Person, pk=pk)
    invoices = person.invoice_set.all()

    return render(request, 'tickets/person_details.html',
                  {'person': person, 'invoices': invoices})


def preemption(request):
    error = ''
    success = False
    liu_id_form = LiuIDForm(request.POST or None)
    ticket_type_form = PreemptionTicketTypeForm(request.POST or None)

    if liu_id_form.is_valid() and ticket_type_form.is_valid():
        try:
            worker = Worker.objects.get(liu_id=liu_id_form.cleaned_data.get('liu_id'))
            if worker.invoice_set.exists():
                raise InvoiceExists()

            invoice = Invoice(person=worker.person_ptr, is_verified=False)
            invoice.generate_data()
            invoice.send_verify_email()
            invoice.save()

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
        invoice.save()

    return render(request, 'tickets/confirm.html')


def create_invoice(person):
    invoice = Invoice(person=person, is_verified=True)
    invoice.generate_data()
    invoice.send_as_email()
    invoice.save()
    return invoice
