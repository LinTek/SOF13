import datetime

from django.db import transaction
from django.db.models import Sum, Count
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required

from sof.functionary.models import Worker, Person

from .models import Invoice, Payment

TRAPPAN_ID = 41


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
def set_paid(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    invoice.payment_set.create(amount=invoice.get_total_price(),
                               date=datetime.date.today())

    return redirect('person_details', pk=invoice.person.pk)


@login_required
@permission_required('tickets.add_invoice')
def send_email(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    invoice.send_as_email()

    return redirect('person_details', pk=invoice.person.pk)


@login_required
@transaction.commit_on_success
def add_trappan(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)

    if not invoice.ticket_set.filter(ticket_type_id=TRAPPAN_ID).exists():
        invoice.ticket_set.create(ticket_type_id=TRAPPAN_ID)
        invoice.send_as_email()

    return redirect('person_details', pk=invoice.person.pk)


@login_required
@permission_required('tickets.add_invoice')
def stats(request):

    unused = (Person.objects
              .annotate(icount=Count('invoice'),
                        wcount=Count('worker__workerregistration'))
              .filter(icount=0, wcount__gt=0).count())

    contracts = (Worker.objects
                 .annotate(wcount=Count('workerregistration'))
                 .filter(wcount__gt=0, contract_approved=False).count())

    workers = (Worker.objects
               .annotate(wcount=Count('workerregistration'))
               .filter(wcount__gt=0).count())

    with_preemption = (Person.objects
                       .annotate(icount=Count('invoice'),
                                 wcount=Count('worker__workerregistration'))
                       .filter(icount__gt=0, wcount__gt=0, worker__contract_approved=False).count())

    unverified = Invoice.objects.filter(is_verified=False).count()
    worth = Invoice.objects.filter(is_verified=True).aggregate(s=Sum('denormalized_total_price'))['s']
    payments = Payment.objects.aggregate(s=Sum('amount'))['s']

    return render(request, 'invoices/stats.html',
                  {'worth': worth, 'payments': payments,
                   'unused': unused, 'unverified': unverified,
                   'contracts': contracts, 'workers': workers,
                   'with_preemption': with_preemption})


@login_required
@permission_required('tickets.add_invoice')
def invoice_list(request):
    invoices = (Invoice.objects
                .select_related('person', 'person__worker', 'person__visitor')
                .prefetch_related('ticket_set', 'ticket_set__ticket_type', 'payment_set'))

    return render(request, 'invoices/invoice_list.html', {'invoices': invoices})
