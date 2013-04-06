# encoding: utf-8
import csv

from django_localflavor_se.forms import SEPersonalIdentityNumberField

from django.conf import settings
from django.core.exceptions import ValidationError

from sof.utils.forms import format_kobra_pid
from sof.utils.kobra_client import KOBRAClient, StudentNotFound, get_kwargs

from sof.functionary.models import Visitor, Person
from sof.tickets.models import Ticket
from sof.invoices.models import Invoice

client = KOBRAClient(settings.KOBRA_USER, settings.KOBRA_KEY)


def format_pid(value):
    try:
        return SEPersonalIdentityNumberField().clean(value)
    except ValidationError:
        return None

workers = 0
manual_visitors = 0
liu_visitors = 0
failed = 0
invalid_pid = 0
no_reason = 0


TYPES = {# TODO ###########################
    'Helhelg': 1,
    'Torsdag': 2,
    'Fredag': 3,
    'Lördag': 4,
}


def try_get_person(pid, liu_id):
    person = None

    if pid:
        try:
            person = Person.objects.search(term=pid)
        except Person.DoesNotExist:
            pass
    elif liu_id:
        try:
            person = Person.objects.search(term=liu_id)
        except Person.DoesNotExist:
            pass

    return person


def try_get_from_kobra(pid, liu_id):
    student = None

    if pid:
        try:
            student = client.get_student_by_pid(pid=format_kobra_pid(pid))
        except StudentNotFound:
            pass
    elif liu_id:
        try:
            student = client.get_student_by_liu_id(liu=liu_id)
        except StudentNotFound:
            pass

    if student:
        return Visitor(**get_kwargs(student))
    return None


def try_create_manually(fname, lname, pid, email):
    if not (fname and lname and email and pid):
        return None

    return Visitor(first_name=fname,
                   last_name=lname,
                   pid=pid,
                   email=email)


def create_tickets(invoice, ticket_types):
    ticket_types = ticket_types.replace(' (tors, fre, lör)', '')
    ticket_type_ids = [TYPES[tt] for tt in ticket_types.split(', ')]

    for ticket_type_id in ticket_type_ids:
        Ticket.objects.create(invoice=invoice, ticket_type_id=ticket_type_id)


with open('people.csv', 'rb') as csvfile:
    def error(msg):
        print
        print msg
        print name
        print ', '.join(row)
        print '-------------------------------'

    reader = csv.reader(csvfile)
    for row in reader:
        _, _, liu_id, name, orig_pid, email, reason, ticket_types = row
        name = unicode(name, 'utf-8')
        name_split = name.split()

        fname, lname = name_split[0], ' '.join(name_split[1:])
        liu_id = liu_id.lower()
        pid = format_pid(orig_pid)

        if not reason:
            error('No reason given')
            no_reason += 1
            continue

        person = try_get_person(pid=pid, liu_id=liu_id)

        if person:
            print 'Existing person'
        else:
            visitor = try_get_from_kobra(pid=pid, liu_id=liu_id)

            if visitor:
                if email:
                    visitor.email = email.lower()
                liu_visitors += 1
            else:
                visitor = try_create_manually(fname, lname, pid, email)

                if visitor:
                    manual_visitors += 1

            if not visitor:
                if orig_pid and not pid:
                    error('Invalid PID')
                    invalid_pid += 1
                    continue
                error('Could not find or create user')
                failed += 1
                continue

            visitor.save()
            person = visitor.person_ptr

        if Invoice.objects.filter(person=person).exists():
            error('Invoice already exists')
            continue

        invoice = Invoice(person=person, is_verified=True)
        invoice.generate_data()
        invoice.save()

        create_tickets(invoice, ticket_types)

    print '\n========================================================'
    print '%d workers' % workers
    print '%d manual visitors' % manual_visitors
    print '%d liu visitors' % liu_visitors
    print '%d failed' % failed
    print '--------------------'
    print '%d invalid PID' % invalid_pid
    print '%d no reason' % no_reason
