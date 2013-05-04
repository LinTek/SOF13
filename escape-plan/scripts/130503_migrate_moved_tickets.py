from sof.invoices.models import Invoice
from sof.functionary.models import Person

for invoice in Invoice.objects.all():
    if invoice.ocr[4:] != invoice.person.pid[2:]:
        try:
            orig_person = Person.objects.get(pid='19%s' % invoice.ocr[4:])
        except Person.DoesNotExist:
            orig_person = None

        print unicode(invoice)
        print "%s -> %s" % (unicode(invoice.person), unicode(orig_person))
        print "------------------------------------------------------------"

        if orig_person:
            invoice.person = orig_person
            invoice.save()
