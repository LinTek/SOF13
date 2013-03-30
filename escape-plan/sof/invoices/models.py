# encoding: utf-8
import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _

from sof.functionary.models import Person


class PaymentStatus:
    NOT_PAID = 'not_paid'
    PAID = 'paid'
    SUM_MISMATCH = 'sum_mismatch'


class Invoice(models.Model):
    class Meta:
        verbose_name = _('invoice')
        verbose_name_plural = _('invoices')

    # is_verified is True if the user has clicked the confirmation link
    is_verified = models.BooleanField(_('is verified'), default=False, blank=True)

    token = models.CharField(max_length=50)
    due_date = models.DateField(_('due date'))
    ocr = models.CharField(_('OCR number'), max_length=20, unique=True)
    person = models.ForeignKey(Person)

    def __unicode__(self):
        return unicode(self.ocr)

    def generate_data(self):
#        self.token = os.urandom(20).encode('hex')
        self.due_date = datetime.date.today() + datetime.timedelta(days=7)
        self.ocr = '5070%s' % self.person.pid  # TODO

    def send_as_email(self):
        pass

    def is_handed_out(self):
        return all([ticket.is_handed_out for ticket in self.ticket_set.all()])

    def get_total_price(self):
        # TODO
        return sum([ticket.price for ticket in self.ticket_set.all()])

    def get_payment_status(self):
        payment_sum = sum([payment.amount for payment in self.payment_set.all()])

        if payment_sum == 0:
            return PaymentStatus.NOT_PAID

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
