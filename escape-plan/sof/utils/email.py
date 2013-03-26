from django.conf import settings

from django.core.mail import send_mail as _django_mail
from django.template.loader import render_to_string


def send_mail(template_name, to, template_params):
    _django_mail(subject=render_to_string('%s_subject.txt' % template_name,
                                          template_params).replace('\n', ''),
                 message=render_to_string('%s.txt' % template_name,
                                          template_params),
              from_email=settings.DEFAULT_FROM_EMAIL, recipient_list=to)
