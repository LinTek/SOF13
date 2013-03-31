from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required

from .models import Invoice


@login_required
@permission_required('tickets.add_ticket')
def set_handed_out(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)

    for ticket in invoice.ticket_set.all():
        ticket.is_handed_out = True
        ticket.save()

    return redirect('person_details', pk=invoice.person.pk)


@login_required
@permission_required('tickets.add_invoice')
def invoice_list(request):
    invoices = Invoice.objects.select_related('person', 'person__worker', 'person__visitor')
    return render(request, 'invoices/invoice_list.html', {'invoices': invoices})
