from sof.invoices.models import Invoice

for invoice in Invoice.objects.filter(is_sent_as_email=False):
    invoice.send_as_email()
