import dkim

from django.core.mail import send_mail as _django_mail
from django.template.loader import render_to_string
from django.core.mail.backends.smtp import EmailBackend
from django.conf import settings


class DKIMBackend(EmailBackend):
    def _send(self, email_message):
        """
        A helper method that does the actual sending + DKIM signing.
        """
        if not email_message.recipients():
            return False
        try:
            message_string = email_message.message().as_string()
            signature = dkim.sign(message_string,
                                  settings.DKIM_SELECTOR,
                                  settings.DKIM_DOMAIN,
                                  settings.DKIM_PRIVATE_KEY)
            self.connection.sendmail(email_message.from_email,
                                     email_message.recipients(),
                                     signature + message_string)
        except:
            if not self.fail_silently:
                raise
            return False
        return True


def send_mail(template_name, to, template_params):
    _django_mail(subject=render_to_string('%s_subject.txt' % template_name,
                                          template_params).replace('\n', ''),
                 message=render_to_string('%s.txt' % template_name,
                                          template_params),
                 from_email=settings.DEFAULT_FROM_EMAIL,
                 recipient_list=to)
