from django.db.models import Count

from sof.functionary.models import Worker
from sof.utils.email import send_mail


for worker in Worker.objects.annotate(shifts=Count('workerregistration')).filter(shifts__gte=2):
    print unicode(worker)
    send_mail('functionary/mail/sommarx', [worker.email], {})

for worker in Worker.objects.filter(super_worker=True):
    print unicode(worker)
    send_mail('functionary/mail/sommarx', [worker.email], {})
