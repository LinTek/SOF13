# encoding: utf-8
from django.db import transaction
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.translation import ugettext_lazy as _

from sof.utils.kobra_client import (KOBRAClient, StudentNotFound, get_kwargs)
from sof.functionary.models import Person
from sof.invoices.models import Invoice

from .models import Ticket, TicketType, Visitor
from .forms import TicketTypeForm, TurboTicketForm, VisitorForm, SearchForm


class InvoiceExists():
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

    tickets = Ticket.objects.order_by('-sell_date')[:10]

    stats = TicketType.objects.active()
    for ticket_type in stats:
        ticket_type.sold = ticket_type.ticket_set.count()

    if turbo_form.is_valid() and ticket_type_form.is_valid():
        client = KOBRAClient(settings.KOBRA_USER, settings.KOBRA_KEY)
        term = turbo_form.cleaned_data.get('term')

        try:
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
                person.username = person.email
                person.save()

            invoice = create_invoice(person)
            ticket_type_id = ticket_type_form.cleaned_data.get('ticket_type')

            Ticket(ticket_type_id=ticket_type_id,
                   invoice=invoice).save()

            return redirect('ticket_sell')

        except StudentNotFound:
            error = _('Student was not found')

        except InvoiceExists:
            error = _('An invoice already exist for this person')

        except ValueError:
            error = _('Could not get the result')

    elif visitor_form.is_valid() and ticket_type_form.is_valid():
        visitor = visitor_form.save(commit=False)
        visitor.username = visitor.email
        create_invoice(visitor)

        Ticket(ticket_type=ticket_type_form.cleaned_data.get('ticket_type'),
               invoice=invoice).save()

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


def person_details(request, pk):
    person = get_object_or_404(Person.objects.select_related('invoices'), pk=pk)
    invoices = person.invoice_set.select_related('tickets')

    return render(request, 'tickets/person_details.html',
                  {'person': person, 'invoices': invoices})


def create_invoice(person):
    invoice = Invoice(person=person)
    invoice.generate_data()
    invoice.send_as_email()
    invoice.save()
    return invoice
