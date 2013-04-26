import datetime
from pytz import timezone

from django.utils import timezone

from sof.invoices.models import Invoice
from sof.utils.email import send_mail
from sof.utils.datetime_utils import sthlm


for invoice in Invoice.objects.filter(is_verified=False):
    tickets = invoice.ticket_set.all()
    print unicode(invoice.person)

    if tickets:
        if timezone.now() - invoice.ticket_set.all()[0].sell_date > datetime.timedelta(hours=24):
            send_mail('invoices/mail/confirm_reminder', [invoice.person.email], {'invoice': invoice})
        else:
            print "Too new"
    else:
        print "No tickets"
