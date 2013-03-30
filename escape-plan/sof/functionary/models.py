# encoding: utf-8
from django.db import models
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User, AbstractUser

from sof.utils.datetime_utils import format_dt, format_time
from sof.utils.email import send_mail
from sof.utils.forms import format_pid


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


class PersonManager(models.Manager):
    def search(self, term):
        return self.filter(Q(liu_id=term) |
                           Q(rfid_number=term) |
                           Q(barcode_number=term) |
                           Q(pid=format_pid(term))).get()


class Person(models.Model):
    pid = models.CharField(_('personal identification number'), max_length=20, unique=True)
    lintek_member = models.BooleanField(blank=True, default=False)
    rfid_number = models.CharField(_('RFID number'), max_length=10, blank=True)
    barcode_number = models.CharField(_('barcode number'), max_length=20, blank=True)
    liu_id = models.CharField(_('LiU ID'), max_length=10, blank=True)

    objects = PersonManager()

    def get_instance(self):
        try:
            return self.worker
        except Worker.DoesNotExist:
            return self.visitor

    def __unicode__(self):
        return unicode(self.get_instance())


class Worker(AbstractUser, Person):
    class Meta:
        verbose_name = _('worker')
        verbose_name_plural = _('workers')
        ordering = ('first_name', 'last_name')

    welcome_email_sent = models.BooleanField(_('welcome email sent'), default=False, blank=True)
    contract_approved = models.BooleanField(_('contract approved'), default=False, blank=True)

    def send_registration_email(self):
        send_mail('functionary/mail/confirm_registrations', [self.email],
                  {'registrations': self.workerregistration_set.select_related('shift').order_by('shift__start'),
                   'worker': self})

    def send_welcome_email(self):
        send_mail('functionary/mail/welcome', [self.email], {})

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
