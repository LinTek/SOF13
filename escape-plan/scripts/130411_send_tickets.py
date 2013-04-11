from sof.invoices.models import Invoice
from sof.tickets.models import Ticket

tickets = Ticket.objects.filter(invoice__is_verified=True)

count = 0

print 'Total: %s' % tickets.count()


for ticket in tickets:
    ticket.send_as_email()
    count += 1

    if not count % 100:
        print count
