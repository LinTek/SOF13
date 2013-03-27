# encoding: utf-8
from django.db import models
from django.utils.translation import ugettext_lazy as _

from sof.functionary.models import Person


class Invoice(models.Model):
    class Meta:
        verbose_name = _('invoice')
        verbose_name_plural = _('invoices')

    # is_verified is True if the user has clicked the confirmation link
    is_verified = models.BooleanField(_('is verified'), default=False, blank=True)
    token = models.CharField(max_length=20)

    due_date = models.DateField(_('due date'))
    ocr = models.CharField(_('OCR number'), max_length=20, unique=True)
    person = models.ForeignKey(Person)

    def __unicode__(self):
        return unicode(self.ocr)


class Payment(models.Model):
    class Meta:
        verbose_name = _('payment')
        verbose_name_plural = _('payments')

    date = models.DateTimeField(_('date'))
    amount = models.DecimalField(_('amount'), decimal_places=2, max_digits=8)
    invoice = models.ForeignKey(Invoice)

    def __unicode__(self):
        return "%s kr, %s" % (self.amount, self.date)
