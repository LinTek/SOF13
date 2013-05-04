from sof.invoices.models import Invoice
from sof.functionary.models import Worker

subjects = 0

for invoice in Invoice.objects.filter(is_verified=True):
    if invoice.get_total_price() != invoice.denormalized_total_price:
        print invoice
        print invoice.person

        subjects += 1

        try:
            invoice.person.worker
            print "Funkis"
        except Worker.DoesNotExist:
            print "Visitor"

        print "-------------------------------------"

print "Total: %d" % subjects
