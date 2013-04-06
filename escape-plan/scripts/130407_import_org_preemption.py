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
    'tovsv238',
    'vicgr847',
    'malle320',
    'sanod536',
    'andjo171',
    'davar111',
    'eliel803',
    'joebj393',
    'kargr302',
    'davha292',
    'jeseh742',
    'sofca260',
    'ronda898',
    'chrth911',
    'mikza835',
    'darbu356',
    'sofer168',
    'albfl803',
    'emekj591',
    'maten763']

# 'cecla781', hittades inte
# 'andpe263', # ENDAGARS

manuals = [
    ('Marica Rehn', '931005-0068', 'rehmar-2@student.ltu.se'),
    ('Albert Bengtsson', '920504-2790', 'albert_789@hotmail.se'),
    ('Joakim Gebart', '860131-7012', 'joakim.gebart@jge.se'),
    (u'Amanda Söderman', '890629-0468', 'amanda.soderman@gmail.com'),
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
