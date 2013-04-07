from sof.invoices.models import Invoice

for invoice in Invoice.objects.filter(is_sent_as_email=False, is_verified=True):
    print unicode(invoice.person)
    invoice.send_as_email()
