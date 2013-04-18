from sof.functionary.models import Worker
from sof.utils.email import send_mail


for worker in Worker.objects.all():
    if worker.workerregistration_set.count() > 0:
        print unicode(worker)
        send_mail('functionary/mail/info', [worker.email],
                  {'registrations': worker.workerregistration_set.all(),
                   'worker': worker})
