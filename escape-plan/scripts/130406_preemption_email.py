#encoding: utf-8
from sof.functionary.models import Worker

for w in Worker.objects.order_by('first_name', 'last_name'):
    w.send_preemption_email()
    print(unicode(w))
