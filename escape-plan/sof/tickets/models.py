# encoding: utf-8
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractUser

from sof.functionary.models import Person
from sof.invoices.models import Invoice


class Visitor(AbstractUser, Person):
    class Meta:
        verbose_name = _('worker')
        verbose_name_plural = _('workers')
        ordering = ('first_name', 'last_name')

    def __unicode__(self):
        return unicode(self.get_full_name())


class TicketType(models.Model):
    class Meta:
        verbose_name = _('ticket type')
        verbose_name_plural = _('ticket types')

    name = models.CharField(_('name'), max_length=50)
    price = models.DecimalField(_('price'), decimal_places=2, max_digits=8)


class Ticket(models.Model):
    class Meta:
        verbose_name = _('ticket')
        verbose_name_plural = _('tickets')

    ticket_type = models.ForeignKey(TicketType)
    invoice = models.ForeignKey(Invoice)
    opening_date = models.DateTimeField(_('opening date'))
    opening_date_public = models.DateTimeField(_('opening date for public selling'))
