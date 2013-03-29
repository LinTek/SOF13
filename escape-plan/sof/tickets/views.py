# encoding: utf-8
from django.db import transaction
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.translation import ugettext_lazy as _

from sof.utils.kobra_client import (KOBRAClient, StudentNotFound, get_kwargs,
                                    get_pid_with_sequel)
from sof.functionary.models import Worker
from sof.invoices.models import Invoice

from .models import Ticket, TicketType, Visitor
from .forms import TicketTypeForm, TurboTicketForm, VisitorForm


@login_required
@permission_required('tickets.add_ticket')
@transaction.commit_on_success
def sell(request):
    error = None

    ticket_type_form = TicketTypeForm(request.POST or None)
    turbo_form = TurboTicketForm(request.POST or None)
    visitor_form = VisitorForm(request.POST or None)

    tickets = Ticket.objects.order_by('-sell_date')[:10]

    stats = TicketType.objects.active()
    for ticket_type in stats:
        ticket_type.sold = ticket_type.ticket_set.count()

    if turbo_form.is_valid() and ticket_type_form.is_valid():
        client = KOBRAClient(settings.KOBRA_USER, settings.KOBRA_KEY)
        term = turbo_form.cleaned_data.get('term')

        try:
            student = client.get_student(term)

            try:
                visitor = Worker.objects.get(pid=get_pid_with_sequel(student))

            except Worker.DoesNotExist():
                visitor = Visitor(**get_kwargs(student))
                visitor.username = visitor.email
                visitor.save()

            invoice = create_invoice(visitor)
            Ticket(ticket_type=ticket_type_form.cleaned_data.get('ticket_type'),
                   invoice=invoice).save()

            return redirect('ticket_sell')

        except StudentNotFound:
            error = _('Student was not found')

        except ValueError:
            error = _('Could not get the result')

    elif visitor_form.is_valid() and ticket_type_form.is_valid():
        visitor = visitor_form.save(commit=False)
        visitor.username = visitor.email
        create_invoice(visitor)

        Ticket(ticket_type=ticket_type_form.cleaned_data.get('ticket_type'),
               invoice=invoice).save()

        return redirect('ticket_sell')

    return render(request, 'tickets/sell.html',
                  {'ticket_type_form': ticket_type_form,
                   'turbo_form': turbo_form,
                   'visitor_form': visitor_form,
                   'latest_tickets': tickets,
                   'ticket_stats': stats,
                   'error': error})


def create_invoice(person):
    invoice = Invoice(person=person)
    invoice.generate_data()
    invoice.send_as_email()
    invoice.save()
    return invoice
