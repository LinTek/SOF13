#encoding: utf-8
from sof.functionary.models import Worker

for w in Worker.objects.filter(welcome_email_sent=False).order_by('first_name', 'last_name'):
    w.send_welcome_email()
    w.welcome_email_sent = True
    w.save()

    print(unicode(w))
