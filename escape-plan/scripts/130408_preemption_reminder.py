from sof.functionary.models import Worker
from sof.utils.email import send_mail


for worker in Worker.objects.all():
    if worker.workerregistration_set.count() > 0:
        if worker.person_ptr.invoice_set.count() == 0:
            print unicode(worker)
            send_mail('preemption_reminder', [worker.email], {})
