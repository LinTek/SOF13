# encoding: utf-8
from django_localflavor_se.forms import SEPersonalIdentityNumberField

from django.db import transaction
from django.conf import settings
from django.core.exceptions import ValidationError

from sof.functionary.models import Visitor
from sof.tickets.models import Ticket
from sof.invoices.models import Invoice
from sof.utils.kobra_client import KOBRAClient, get_kwargs


def format_pid(value):
    try:
        return SEPersonalIdentityNumberField().clean(value)
    except ValidationError:
        return None

liu_ids = [
    'fanra741',
    'bjoli467',
    'erima666',
    'patan156',
    'chrma532',
    'bjoli638',
    'aleja404',
    'anthe862',
    'ottca427',
    'hedde211',
]

# 'cecla781', hittades inte
# 'andpe263', # ENDAGARS

manuals = [
    ('Henrik Olofsson', '880708-0257', 'treffin@gmail.com'),
    ('Viktor Boronsved', '890212-2533', 'viktor.borensved@jm.se'),
]

client = KOBRAClient(settings.KOBRA_USER, settings.KOBRA_KEY)


@transaction.commit_on_success
def main():
    def create_stuff():
        invoice = Invoice(person=visitor.person_ptr, is_verified=True)
        invoice.generate_data()
        invoice.save()
        Ticket.objects.create(invoice=invoice, ticket_type_id=1)

    for liu_id in liu_ids:
        print liu_id

        student = client.get_student_by_liu_id(liu=liu_id)

        visitor = Visitor.objects.create(**get_kwargs(student))
        print unicode(visitor)
        create_stuff()

    for name, pid, email in manuals:
        name_split = name.split()
        fname, lname = name_split[0], ' '.join(name_split[1:])

        visitor = Visitor.objects.create(first_name=fname,
                                         last_name=lname,
                                         pid=format_pid(pid),
                                         email=email)
        print unicode(visitor)
        create_stuff()

main()
