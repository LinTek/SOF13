from django.db import models
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.models import User, AbstractUser


class ShiftType(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name


class Shift(models.Model):
    start = models.DateTimeField(_('start date'))
    end = models.DateTimeField(_('end date'))
    max_workers = models.PositiveSmallIntegerField(_('max workers'))
    shift_type = models.ForeignKey('ShiftType')
    responsible_person = models.ForeignKey(User)

    def __unicode__(self):
        return '{0} {1}-{2}'.format(unicode(self.shift_type), self.start, self.end)


class Functionary(AbstractUser):
    liu_id = models.CharField(_('LiU-ID'), max_length=8, blank=True)
    liu_card_number = models.CharField(_('LiU card number'), max_length=30, blank=True)


class WorkerRegistration(models.Model):
    worker = models.ForeignKey(User)
    shift = models.ForeignKey(Shift)
    approved = models.BooleanField(_('approved'), default=False)
