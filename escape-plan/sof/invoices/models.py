# encoding: utf-8
from django.db import models
from django.utils.translation import ugettext_lazy as _

from sof.tickets.models import Ticket


class Payment(models.Model):
    class Meta:
        verbose_name = _('payment')
        verbose_name_plural = _('payments')

    date = models.DateTimeField(_('date'))
    amount = models.DecimalField(_('amount'), decimal_places=2, max_digits=8)


class Invoice(models.Model):
    class Meta:
        verbose_name = _('invoice')
        verbose_name_plural = _('invoices')

    tickets = models.ManyToManyField(Ticket)
    payments = models.ManyToManyField(Payment)
