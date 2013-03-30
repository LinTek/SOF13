# encoding: utf-8
from django import template
from django.utils.translation import ugettext as _

from sof.invoices.models import PaymentStatus

register = template.Library()

PAYMENTS = {
    PaymentStatus.PAID: ('label-success', _('Paid')),
    PaymentStatus.SUM_MISMATCH: ('label-warning', _('Sum mismatch')),
    PaymentStatus.NOT_PAID: ('label-important', _('Not paid')),
}

HANDED_OUT = {
    True: ('label-important', _('Already handed out')),
    False: ('label-success', _('Not handed out')),
}


@register.inclusion_tag('tickets/partials/status_label.html')
def payment_status(status):
    label, text = PAYMENTS[status]
    return {'class': label, 'text': text}


@register.inclusion_tag('tickets/partials/status_label.html')
def handed_out_status(handed_out):
    label, text = HANDED_OUT[handed_out]
    return {'class': label, 'text': text}
