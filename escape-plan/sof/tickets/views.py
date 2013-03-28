from django.utils.timezone import now

from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required

from .models import TicketType


@login_required
@permission_required('tickets.add_ticket')
def ticket_search(request):
    ticket_types = TicketType.objects.filter(opening_date__lte=now())

    return render(request, 'tickets/search.html', {'ticket_types': ticket_types})
