# encoding: utf-8
from django.db import models
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _

from sof.invoices.models import Invoice


class TicketTypeManager(models.Manager):
    def active(self):
        return self.filter(opening_date__lte=now())

    def public(self):
        return self.filter(opening_date_public__lte=now())


class TicketType(models.Model):
    class Meta:
        verbose_name = _('ticket type')
        verbose_name_plural = _('ticket types')

    name = models.CharField(_('name'), max_length=50)
    price = models.DecimalField(_('price'), decimal_places=2, max_digits=8)
    price_rebate = models.DecimalField(_('rebate price'), decimal_places=2, max_digits=8)

    max_amount = models.PositiveIntegerField(_('max amount'))
    opening_date = models.DateTimeField(_('opening date'))
    opening_date_public = models.DateTimeField(_('opening date for public selling'))

    objects = TicketTypeManager()

    def __unicode__(self):
        return unicode(self.name)


class Ticket(models.Model):
    class Meta:
        verbose_name = _('ticket')
        verbose_name_plural = _('tickets')

    ticket_type = models.ForeignKey(TicketType)
    sell_date = models.DateTimeField(auto_now_add=True)
    invoice = models.ForeignKey(Invoice)
    is_handed_out = models.BooleanField(_('handed out'), default=False, blank=True)

    def __unicode__(self):
        return unicode("%s #%d" % (unicode(self.ticket_type), self.id))
