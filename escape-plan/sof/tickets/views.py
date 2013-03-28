# encoding: utf-8
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required

from .models import Ticket, TicketType
from .forms import TurboTicketForm


@login_required
@permission_required('tickets.add_ticket')
def ticket_search(request):
    turbo_form = TurboTicketForm()
    tickets = Ticket.objects.order_by('-sell_date')[:10]

    stats = TicketType.objects.active()
    for ticket_type in stats:
        ticket_type.sold = ticket_type.ticket_set.count()

    return render(request, 'tickets/search.html',
                  {'turbo_form': turbo_form,
                   'latest_tickets': tickets,
                   'ticket_stats': stats})
