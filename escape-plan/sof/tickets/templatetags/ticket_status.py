# encoding: utf-8
from django import template
from django.utils.translation import ugettext_lazy as _

from sof.invoices.models import PaymentStatus

register = template.Library()

STYLES = {
    PaymentStatus.PAID: 'label-success',
    PaymentStatus.SUM_MISMATCH: 'label-warning',
    PaymentStatus.NOT_PAID: 'label-important',
}

TEXTS = {
    PaymentStatus.PAID: _('Paid'),
    PaymentStatus.SUM_MISMATCH: _('Sum mismatch'),
    PaymentStatus.NOT_PAID: _('Not paid'),
}

@register.inclusion_tag('tickets/partials/status_label.html')
def payment_status(status):
    return {'class': STYLES[status], 'text': TEXTS[status]}


@register.inclusion_tag('tickets/partials/status_label.html')
def handed_out_status(handed_out):
    if handed_out:
        return {'class': 'label-success', 'text': _('Handed out')}
    return {'class': 'label-important', 'text': _('Not handed out')}
