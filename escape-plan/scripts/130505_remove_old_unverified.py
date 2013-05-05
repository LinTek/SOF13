import datetime

from sof.invoices.models import Invoice
from sof.utils.datetime_utils import sthlm


for invoice in Invoice.objects.filter(is_verified=False):
    tickets = invoice.ticket_set.all()

    if tickets:
        if invoice.is_sent_as_email:
            print 'Is sent: %s' % unicode(invoice.person)

        elif invoice.ticket_set.all()[0].sell_date < sthlm.localize(datetime.datetime(2013, 4, 25, 0, 0)):
            invoice.delete()
            print 'Deleted: %s' % unicode(invoice.person)
