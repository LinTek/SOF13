# encoding: utf-8
"""
views.py

A view is called when a visited url-entry in urls.py points to it.
They must return a HTTPResponse-object, which often is a rendered view or
redirect. Views typically creates and saves form instances, fetches stuff
from database or calls methods on models. Be careful not to do too much
work in the views to maintain a somewhat good MVC-pattern.
"""
from collections import defaultdict
from itertools import groupby

from django.db.models import Count, Q
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from forms import OrchestraForm, MemberForm, AddMemberForm
from models import Orchestra, Member, YES, TICKET_TYPES, GADGETS, TSHIRT_SIZES


def home(request):
    return redirect('orchestra_form')


def confirm_member(request):
    return render(request, 'orkester/confirm_member.html')


def confirm_orchestra(request):
    return render(request, 'orkester/confirm_orchestra.html')


def orchestra_form(request):
    # if we are submittning a form
    if request.method == 'POST':
        # create a form filled with the sent POST-data
        form = OrchestraForm(request.POST, request.FILES)

        # if the form was filled-in correctly
        if form.is_valid():
            # save the orchestra in memory, but not write it to database yet
            # since we want to assign a token for the orchestra first
            orchestra = form.save(commit=False)
            # generate a token (that work is done in the model)
            orchestra.generate_token()
            # save to database and send an confirmation e-mail
            orchestra.save()
            orchestra.send_confirm_email()

            return redirect('confirm_orchestra')

    # otherwise, if we just visit the form for the first time
    else:
        # create a new, empty form
        form = OrchestraForm()

    return render(request, 'orkester/orchestra_form.html', {'form': form})


def member_form(request, token):
    # fetch the orchestra from db by the token in the URL
    orchestra = _orchestra_by_token(token)

    if request.method == 'POST':
        form = MemberForm(request.POST)

        if form.is_valid():
            member = form.save()
            member.orchestras.add(orchestra)
            member.late_registration = True
            member.save()

            member.send_confirm_email(orchestra)

            return redirect('confirm_member')
    else:
        form = MemberForm()

    return render(request, 'orkester/member_form.html',
                  {'form': form, 'orchestra': orchestra})


def member_list(request, token):
    orchestra = _orchestra_by_token(token)
    # member_set is a so-called backwards relation, which allows us to get
    # all the orchestra members which belongs to a certain orchestra.
    members = orchestra.member_set.order_by('first_name', 'last_name')

    return render(request, 'orkester/member_list.html',
                  {'orchestra': orchestra, 'members': members})


@login_required
def press_list(request):
    orchestras = Orchestra.objects.order_by('orchestra_name')
    fields = ('orchestra_name', 'sof_count', 'look_forward_to', 'music_type',
              'best_memory', 'rituals', 'three_words', 'showpiece', 'best_with_sof',
              'why_orchestra', 'craziest_thing', 'determines_repertory', 'what_do_you_do',
              'uniform_description', 'dance', 'thing_to_bring', 'mottos', 'orchestra_image',
              'logo_image')

    return render(request, 'orkester/orchestra_list.html',
                  {'orchestras': orchestras, 'fields': fields})


@login_required
def orchestra_list(request):
    orchestras = Orchestra.objects.order_by('orchestra_name')
    fields = (
        'orchestra_name', 'short_name', 'use_short_name', 'music_type',
        'showpiece', 'departure_day', 'parking_lot_needed', 'parking_lot_type',
        'estimated_instruments', 'play_thursday', 'play_friday', 'concerto_preludium',
        'concerto_grosso', 'family_play', 'backline', 'amplifier_guitar', 'amplifier_bass',
        'uses_drumset', 'will_bring_drumset', 'uses_piano', 'microphones', 'ballet_name',
        'message', 'primary_contact_email', 'ballet_contact_email')

    return render(request, 'orkester/orchestra_list.html',
                  {'orchestras': orchestras, 'fields': fields})


@login_required
def attends_10_25_list(request):
    members = (Member.objects
               .filter(Q(attends_10th_year=True) | Q(attends_25th_time=True))
               .order_by('first_name', 'last_name'))

    return render(request, 'orkester/attends_10_25_list.html',
                  {'members': members})


def _group(lst, f):
    return [(group, list(members)) for group, members in groupby(lst, key=f)]


@login_required
def food_list(request, day=None):
    if not day:
        return render(request, 'orkester/food_list.html')

    day_name = {'thursday': 'torsdag', 'friday': 'fredag', 'saturday': 'lördag', 'sunday': 'söndag'}[day]

    days = {'thursday': ('thursday',),
            'friday': ('thursday', 'friday'),
            'saturday': ('thursday', 'friday', 'saturday'),
            'sunday': ('thursday', 'friday')}

    types = days[day]

    orchestras = Orchestra.objects.order_by('orchestra_name')
    member_list = defaultdict(lambda: defaultdict(int))

    for member in Member.objects.select_related('orchestras').order_by('first_name', 'last_name'):
        if member.ticket_type in types:
            orchestra = member.orchestras.order_by('id').all()[0]
            member_list[orchestra.pk]['total'] += 1

            if member.allergies:
                if not member_list[orchestra.pk]['allergies']:
                    member_list[orchestra.pk]['allergies'] = []

                member_list[orchestra.pk]['allergies'].append(member)

    total = 0
    for orchestra in orchestras:
        orchestra.total = member_list[orchestra.pk]['total']
        orchestra.allergies = member_list[orchestra.pk]['allergies']
        total += orchestra.total

    return render(request, 'orkester/food_list.html',
                  {'orchestras': orchestras, 'day_name': day_name, 'total': total})


@login_required
def stats(request):
    T_SHIRTS = [('t_shirt_%s' % s, 'T-shirt (%s)' % s) for s, s in TSHIRT_SIZES]

    all_total_fields = (['members', 'sitting', 'bed', 'kartege'] +
                        [t for t, _ in T_SHIRTS] +
                        [t for t, _ in TICKET_TYPES] +
                        [t for t, _ in GADGETS])
    orchestras = (Orchestra.objects.order_by('orchestra_name')
                                   .select_related('member')
                                   .annotate(member_count=Count('member')))

    sums = defaultdict(lambda: defaultdict(int))

    for member in Member.objects.select_related('orchestras'):
        orchestra = member.orchestras.order_by('id').all()[0]

        sums[orchestra.pk]['members'] += 1
        sums[orchestra.pk][member.ticket_type] += 1
        # The summation below is actually quite obscure and based on the fact that
        # True and False is evaluated as 1 and 0 respectively.
        sums[orchestra.pk]['sitting'] += member.attend_sitting == YES
        sums[orchestra.pk]['bed'] += member.needs_bed == YES
        sums[orchestra.pk]['kartege'] += member.plays_kartege == YES

        for gtype, _ in GADGETS:
            sums[orchestra.pk][gtype] += getattr(member, gtype)

        if member.t_shirt:
            sums[orchestra.pk]['t_shirt_%s' % member.t_shirt_size] += 1

    totals = defaultdict(int)
    for orchestra in orchestras:
        orchestra.totals = sums[orchestra.pk]

        for e in all_total_fields:
            totals[e] += orchestra.totals[e]

    return render(request, 'orkester/stats.html',
                  {'orchestras': orchestras,
                   'totals': totals,
                   'ticket_types': TICKET_TYPES,
                   'gadget_types': GADGETS + T_SHIRTS})


def add_member(request, token):
    orchestra = _orchestra_by_token(token)

    if request.method == 'POST':
        form = AddMemberForm(request.POST)

        if form.is_valid():
            # get the personal id number from the form
            pid = form.cleaned_data.get('pid')
            # fetch that member from db
            member = Member.objects.get(pid=pid)
            # add the orchestra to the set of the member's orchestras
            member.orchestras.add(orchestra)

            member.late_registration = True
            member.save()

            member.send_confirm_email(orchestra)

            return redirect('confirm_member')
    else:
        form = AddMemberForm()

    return render(request, 'orkester/add_member_form.html',
                  {'form': form, 'orchestra': orchestra})


def _orchestra_by_token(token):
    """
    Helper function which just fetches an orchestra from a token or raises
    HTTP 404 is not found.
    """
    return get_object_or_404(Orchestra, token=token)
