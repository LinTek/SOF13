# encoding: utf-8
from sof.invoices.models import Invoice
from sof.tickets.models import Ticket

for invoice in Invoice.objects.all():
    Ticket.objects.create(ticket_type_id=1, invoice=invoice)
    print '%s <%s>, ' % (unicode(invoice.person), invoice.person.email),
