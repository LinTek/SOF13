# encoding: utf-8
import os
import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _

from sof.functionary.models import Person, Worker
from sof.utils.email import send_mail
from sof.utils.forms import format_kobra_pid


class PaymentStatus:
    NOT_PAID = 'not_paid'
    PAID = 'paid'
    SUM_MISMATCH = 'sum_mismatch'
    OVERDUE = 'overdue'


class Invoice(models.Model):
    class Meta:
        verbose_name = _('invoice')
        verbose_name_plural = _('invoices')

    # is_verified is True if the user has clicked the confirmation link
    is_verified = models.BooleanField(_('is verified'), default=False, blank=True)

    token = models.CharField(max_length=50, unique=True, db_index=True)
    due_date = models.DateField(_('due date'))
    ocr = models.CharField(_('OCR number'), max_length=20, unique=True)
    person = models.ForeignKey(Person)

    is_sent_as_email = models.BooleanField(_('is sent as email'), default=False, blank=True)
    denormalized_total_price = models.DecimalField(decimal_places=2, max_digits=8, default=0)

    def __unicode__(self):
        return unicode(self.ocr)

    def generate_data(self):
        self.token = os.urandom(20).encode('hex')
        self.due_date = datetime.date.today() + datetime.timedelta(days=7)
        self.ocr = 'sof-%s' % format_kobra_pid(self.person.pid, dash=False)

    def send_as_email(self):
        send_mail('invoices/mail/invoice', [self.person.email], {'invoice': self})
        self.is_sent_as_email = True
        self.denormalized_total_price = self.get_total_price()
        self.save()

    def send_verify_email(self):
        send_mail('invoices/mail/preemption', [self.person.email], {'invoice': self})

    def is_handed_out(self):
        return all([ticket.is_handed_out for ticket in self.ticket_set.all()])

    def get_total_ticket_sum(self):
        if self.person.has_rebate():
            return sum([ticket.ticket_type.price_rebate for ticket in self.ticket_set.all()])
        return sum([ticket.ticket_type.price for ticket in self.ticket_set.all()])

    def get_payment_sum(self):
        return sum([payment.amount for payment in self.payment_set.all()])

    def get_total_price(self):
        try:
            rebate_percent = self.person.worker.get_rebate_percent()
        except Worker.DoesNotExist:
            rebate_percent = 0

        return self.get_total_ticket_sum() * (1 - rebate_percent)

    def get_payment_status(self):
        payment_sum = self.get_payment_sum()
        if payment_sum == 0:
            if self.due_date >= datetime.date.today():
                return PaymentStatus.NOT_PAID
            return PaymentStatus.OVERDUE

        if self.get_total_price() == payment_sum:
            return PaymentStatus.PAID

        return PaymentStatus.SUM_MISMATCH


class Payment(models.Model):
    class Meta:
        verbose_name = _('payment')
        verbose_name_plural = _('payments')

    date = models.DateTimeField(_('date'))
    amount = models.DecimalField(_('amount'), decimal_places=2, max_digits=8)
    invoice = models.ForeignKey(Invoice)

    def __unicode__(self):
        return "%s kr, %s" % (self.amount, self.date)
