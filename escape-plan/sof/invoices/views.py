from django.shortcuts import redirect, get_object_or_404

from .models import Invoice


def set_handed_out(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)

    for ticket in invoice.ticket_set.all():
        ticket.is_handed_out = True
        ticket.save()

    return redirect('person_details', pk=invoice.person.pk)
