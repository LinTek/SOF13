#encoding: utf-8
from sof.functionary.models import Worker
from sof.utils.email import send_mail


for w in Worker.objects.order_by('first_name', 'last_name'):
    send_mail('functionary/mail/welcome2', [w.email], {})

    print(unicode(w))
