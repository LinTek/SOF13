from sof.invoices.models import Invoice

for invoice in Invoice.objects.all():
    if len(invoice.ocr) == 16:
        invoice.ocr = 'sof-%s' % invoice.ocr[6:]
        invoice.save()
