from sof.invoices.models import Invoice, PaymentStatus

invoices = (Invoice.objects
            .select_related('person', 'person__worker', 'person__visitor')
            .prefetch_related('ticket_set', 'ticket_set__ticket_type', 'payment_set'))

for invoice in invoices:
    if invoice.get_payment_status() == PaymentStatus.OVERDUE:
        invoice.send_nice_reminder()
