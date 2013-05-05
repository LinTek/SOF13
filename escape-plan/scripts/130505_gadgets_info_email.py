#encoding: utf-8
from sof.functionary.models import Worker
from sof.utils.email import send_mail


for w in Worker.objects.filter(fetched_merchandise=False):
    if worker.workerregistration_set.count() > 0:
        print(unicode(w))
        send_mail('functionary/mail/gadgets_info', [w.email], {})
