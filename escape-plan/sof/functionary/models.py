from django.db import models
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.models import User, AbstractUser
from django.db.models import Count


class ShiftType(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name


class ShiftManager(models.Manager):
    def with_free_places(self):
        res = []
        shifts = (self.order_by('shift_type', 'start')
                      .annotate(worker_count=Count('workerregistration')))

        # There is unfortunately no good way to do this without using raw SQL...
        for shift in shifts:
            free_places = shift.max_workers - shift.worker_count

            if free_places > 0:
                shift.free_places = free_places
                res.append(shift)
        return res


class Shift(models.Model):
    objects = ShiftManager()

    start = models.DateTimeField(_('start date'))
    end = models.DateTimeField(_('end date'))
    max_workers = models.PositiveSmallIntegerField(_('max workers'))
    shift_type = models.ForeignKey('ShiftType')
    responsible_person = models.ForeignKey(User)

    def __unicode__(self):
        return '{0} | {1} - {2}'.format(unicode(self.shift_type),
                                    format_dt(self.start), format_dt(self.end))


class Worker(AbstractUser):
    liu_id = models.CharField(_('LiU-ID'), max_length=8, blank=True)
    liu_card_number = models.CharField(_('LiU card number'), max_length=30, blank=True)


class WorkerRegistration(models.Model):
    worker = models.ForeignKey(User)
    shift = models.ForeignKey(Shift)
    approved = models.BooleanField(_('approved'), default=False)

    def __unicode__(self):
        return '{0} @ {1}'.format(unicode(self.worker), unicode(self.shift))


def format_dt(dt):
    return dt.strftime('%d %b %H:%M')
