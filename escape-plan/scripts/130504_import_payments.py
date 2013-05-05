# encoding: utf-8
from decimal import Decimal
import datetime

from sof.invoices.models import Invoice, PaymentStatus


with open('payments.csv', 'rU') as csvfile:
    def error(emessage):
        print emessage
        print row

    for row in csvfile:
        message, _, amount = row.split(';')[:3]
        message = message.strip().lower()

        if not (len(message) == 14 and message.startswith('sof-')):
            error("Unparsable payment row")
            continue

        amount = Decimal(amount)

        try:
            invoice = Invoice.objects.get(ocr=message)

        except Invoice.DoesNotExist:
            error("Could not find invoice")
            continue

        if invoice.get_payment_status() == PaymentStatus.PAID:
            continue

        invoice.payment_set.create(date=datetime.date(2013, 05, 02),
                                   amount=amount)
