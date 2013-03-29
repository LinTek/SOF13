# encoding: utf-8
from django.db import transaction
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.translation import ugettext_lazy as _

from sof.utils.kobra_client import KOBRAClient, StudentNotFound, get_kwargs
from sof.invoices.models import Invoice

from .models import Ticket, TicketType, Visitor
from .forms import TurboTicketForm


@login_required
@permission_required('tickets.add_ticket')
@transaction.commit_on_success
def ticket_search(request):
    error = None
    turbo_form = TurboTicketForm(request.POST or None)
    tickets = Ticket.objects.order_by('-sell_date')[:10]

    stats = TicketType.objects.active()
    for ticket_type in stats:
        ticket_type.sold = ticket_type.ticket_set.count()

    if turbo_form.is_valid():
        client = KOBRAClient(settings.KOBRA_USER, settings.KOBRA_KEY)
        term = turbo_form.cleaned_data.get('term')

        try:
            visitor = Visitor(**get_kwargs(client.get_student(term)))
            visitor.save()

            invoice = Invoice(person=visitor)
            invoice.generate_data()
            invoice.send_as_email()
            invoice.save()

            Ticket(ticket_type=turbo_form.cleaned_data.get('ticket_type'),
                   invoice=invoice).save()

            return redirect('ticket_search')

        except StudentNotFound:
            error = _('Student was not found')

        except ValueError:
            error = _('Could not get the result')

    return render(request, 'tickets/search.html',
                  {'turbo_form': turbo_form,
                   'latest_tickets': tickets,
                   'ticket_stats': stats,
                   'error': error})
