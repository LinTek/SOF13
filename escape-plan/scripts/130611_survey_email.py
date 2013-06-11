from sof.functionary.models import Worker
from sof.utils.email import send_mail


for worker in Worker.objects.all():
    regs = worker.workerregistration_set.all()

    if len(regs) > 0:
        print unicode(worker)
        send_mail('functionary/mail/survey', [worker.email], {})
