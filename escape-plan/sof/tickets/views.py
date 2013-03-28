from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required


@login_required
@permission_required('tickets.add_ticket')
def ticket_search(request):
    return render(request, 'tickets/search.html', {})
