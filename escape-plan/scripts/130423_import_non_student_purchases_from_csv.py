# coding: utf-8
import csv

from django.conf import settings
from django.core.exceptions import ValidationError

from sof.utils.forms import format_kobra_pid, ForgivingPIDField
from sof.utils.kobra_client import KOBRAClient, StudentNotFound, get_kwargs

from sof.functionary.models import Visitor, Person
from sof.tickets.models import Ticket
from sof.invoices.models import Invoice


def format_pid(value):
    try:
        return ForgivingPIDField().clean(value)
    except ValidationError:
        return None

TYPES = {
    'Helhelg / Weekend': 1,
    'Torsdag / Thursday': 11,
    'Fredag / Friday': 21,
    'Lördag / Saturday': 31,
}

def try_get_person(pid):
    person = None
    if pid:
        try:
            person = Person.objects.get(pid=pid)
        except Person.DoesNotExist:
            pass
    return person


def create_tickets(invoice, ticket_types):
    ticket_type_ids = [TYPES[tt] for tt in ticket_types.split(', ')]

    for ticket_type_id in ticket_type_ids:
        ticket = Ticket.objects.create(invoice=invoice, ticket_type_id=ticket_type_id)
        ticket.send_as_email()


def try_create_manually(fname, lname, pid, email):
    if not (fname and lname and email and pid):
        return None

    return Visitor(first_name=fname,
                   last_name=lname,
                   pid=pid,
                   email=email)


with open('non_students.csv', 'rb') as csvfile:
    def error(msg):
        print
        print msg
        print ' '.join((first_name, last_name))
        print ', '.join(row)
        print '-------------------------------'

    reader = csv.reader(csvfile)

    for row in reader:
        _, ticket_types, first_name, last_name, orig_pid, email, status = row
        email = email.lower()

        if not status == "Redo för import":
            continue

        pid = format_pid(orig_pid)

        if try_get_person(pid=pid):
            error('Person exists')
            continue

        person = try_create_manually(first_name, last_name, pid, email)

        if not person:
            error('Could not create person')
            continue

        person.save()
        print ' '.join((first_name, last_name))

        invoice = Invoice(person=person, is_verified=True)
        invoice.generate_data()
        invoice.save()

        create_tickets(invoice, ticket_types)
        invoice.send_as_email()
