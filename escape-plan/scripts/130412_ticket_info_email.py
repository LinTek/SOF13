from sof.invoices.models import Invoice
from sof.utils.email import send_mail


invoices = Invoice.objects.filter(is_verified=True).select_related('person')
count = 0
print 'Total: %s' % invoices.count()


for invoice in invoices:
    send_mail('tickets/mail/ticket_info', [invoice.person.email], {})
    count += 1

    if not count % 100:
        print count
