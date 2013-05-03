from sof.functionary.models import Worker
from sof.utils.email import send_mail


for worker in Worker.objects.all():
    if worker.workerregistration_set.count() > 0 or worker.super_worker or worker.orchestra_worker:
        print unicode(worker)
        send_mail('functionary/mail/info_meeting_reminder', [worker.email], {})
