# encoding: utf-8
from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User, AbstractUser
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.shortcuts import redirect


class ShiftType(models.Model):
    class Meta:
        verbose_name = _('shift type')
        verbose_name_plural = _('shift types')

    name = models.CharField(max_length=100)

    def __unicode__(self):
        return unicode(self.name)


class ShiftManager(models.Manager):
    def with_free_places(self, worker):
        res = []
        shifts = (self.order_by('shift_type', 'start')
                      .select_related('shift_type')
                      .prefetch_related('workerregistration_set')
                      .annotate(worker_count=models.Count('workerregistration')))

        try:
            registrations = set(worker.workerregistration_set.all())
        except AttributeError:
            registrations = None

        # There is unfortunately no good way to do this without using raw SQL...
        for shift in shifts:
            free_places = shift.max_workers - shift.worker_count
            if registrations:
                shift.worker_is_signed_up = bool(
                    registrations.intersection(set(shift.workerregistration_set.all())))

            if free_places > 0:
                shift.free_places = free_places
                res.append(shift)
        return res


class Shift(models.Model):
    class Meta:
        verbose_name = _('shift')
        verbose_name_plural = _('shifts')

    objects = ShiftManager()

    start = models.DateTimeField(_('start date'))
    end = models.DateTimeField(_('end date'))
    max_workers = models.PositiveSmallIntegerField(_('max workers'))
    shift_type = models.ForeignKey('ShiftType')
    responsible_person = models.ForeignKey(User)

    def __unicode__(self):
        return '%s | %s - %s' % (unicode(self.shift_type),
                                 format_dt(self.start), format_time(self.end))


class Worker(AbstractUser):
    class Meta:
        verbose_name = _('worker')
        verbose_name_plural = _('workers')

    pid = models.CharField(_('personal identification number'), max_length=20, unique=True)

    def send_registration_email(self):
        _mail('confirm_registrations', [self.email],
                {'registrations': self.workerregistration_set.select_related('shift').all(),
                 'worker': self})
        return redirect('search')

    def __unicode__(self):
        return unicode(self.get_full_name())


class WorkerRegistration(models.Model):
    class Meta:
        verbose_name = _('worker registration')
        verbose_name_plural = _('worker registrations')

    worker = models.ForeignKey(Worker)
    shift = models.ForeignKey(Shift)
    approved = models.BooleanField(_('approved'), default=False)

    def __unicode__(self):
        return '%s @ %s' % (unicode(self.worker), unicode(self.shift))


def format_dt(dt):
    return dt.strftime('%d %b, kl %H:%M')


def format_time(dt):
    return dt.strftime('kl %H:%M')


def _mail(template_name, to, template_params):
    send_mail(subject=render_to_string('functionary/mail/%s_subject.txt' % template_name,
                                       template_params).replace('\n', ''),
              message=render_to_string('functionary/mail/%s.txt' % template_name,
                                       template_params),
              from_email=settings.DEFAULT_FROM_EMAIL, recipient_list=to)
