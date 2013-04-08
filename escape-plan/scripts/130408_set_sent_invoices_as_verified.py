from sof.invoices.models import Invoice

for invoice in Invoice.objects.filter(is_sent_as_email=True, is_verified=False):
    print unicode(invoice.person)
    invoice.is_verified = True
    invoice.save()
