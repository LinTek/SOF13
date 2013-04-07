from sof.functionary.models import Worker, Shift
from sof.invoices.models import Invoice

for w in Worker.objects.filter(contract_approved=False):
    try:
        invoice = w.invoice_set.get()

        if invoice.is_sent_as_email and w.workerregistration_set.count() > 1:
            print "%s <%s>, " % (unicode(w), w.email)

    except Invoice.DoesNotExist:
        pass

print "======= Superfunkis ======="

for r in Shift.objects.get(pk=1301).workerregistration_set.all():  # superfunkis
    w = r.worker

    try:
        invoice = w.invoice_set.get()
        print "%s <%s>, " % (unicode(w), w.email)
    except Invoice.DoesNotExist:
        pass
