# encoding: utf-8
from pytz import timezone

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.dateformat import format
from django.contrib.auth.models import User, AbstractUser
from django.core.mail import send_mail
from django.template.loader import render_to_string

sthlm = timezone('Europe/Stockholm')


class ShiftManager(models.Manager):
    def with_free_places(self, worker=None):
        res = []
        shifts = (self.order_by('shift_type', 'start')
                      .select_related('shift_type', 'shift_sub_type')
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


class ShiftType(models.Model):
    class Meta:
        verbose_name = _('shift type')
        verbose_name_plural = _('shift types')
        ordering = ('name',)

    name = models.CharField(max_length=100)

    def __unicode__(self):
        return unicode(self.name)


class ShiftSubType(models.Model):
    class Meta:
        verbose_name = _('shift subtype')
        verbose_name_plural = _('shift subtypes')
        ordering = ('name',)

    name = models.CharField(max_length=100)

    def __unicode__(self):
        return unicode(self.name)


class Shift(models.Model):
    class Meta:
        verbose_name = _('shift')
        verbose_name_plural = _('shifts')

    objects = ShiftManager()

    start = models.DateTimeField(_('start date'))
    end = models.DateTimeField(_('end date'))
    max_workers = models.PositiveSmallIntegerField(_('max workers'))
    shift_type = models.ForeignKey('ShiftType')
    shift_sub_type = models.ForeignKey('ShiftSubType', null=True, blank=True)
    responsible_person = models.ForeignKey(User, null=True, blank=True)
    is_dummy = models.BooleanField(_('dummy shift'), default=False, blank=True)

    def __unicode__(self):
        return '%s, %s-%s' % (unicode(self.shift_type), format_dt(self.start), format_time(self.end))


class Worker(AbstractUser):
    class Meta:
        verbose_name = _('worker')
        verbose_name_plural = _('workers')
        ordering = ('first_name', 'last_name')

    pid = models.CharField(_('personal identification number'), max_length=20, unique=True)
    welcome_email_sent = models.BooleanField(_('welcome email sent'), default=False, blank=True)

    def send_registration_email(self):
        _mail('confirm_registrations', [self.email],
              {'registrations': self.workerregistration_set.select_related('shift').order_by('shift__start'),
              'worker': self})

    def send_welcome_email(self):
        _mail('welcome', [self.email], {})

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
    return format(dt.astimezone(sthlm), 'l d F H:i')


def format_time(dt):
    return format(dt.astimezone(sthlm), 'H:i')


def _mail(template_name, to, template_params):
    send_mail(subject=render_to_string('functionary/mail/%s_subject.txt' % template_name,
                                       template_params).replace('\n', ''),
              message=render_to_string('functionary/mail/%s.txt' % template_name,
                                       template_params),
              from_email=settings.DEFAULT_FROM_EMAIL, recipient_list=to)
