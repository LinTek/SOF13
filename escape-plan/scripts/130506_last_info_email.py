import datetime

from sof.functionary.models import Worker
from sof.utils.email import send_mail


for worker in Worker.objects.all():
    regs = worker.workerregistration_set.all()

    if len(regs) > 0:
        print unicode(worker)

        if len(regs) == 1 and regs[0].shift.start.date() == datetime.date(2013, 5, 6):
            print "- Skipping..."
            continue

        send_mail('functionary/mail/last_info', [worker.email],
                  {'registrations': regs, 'worker': worker})
