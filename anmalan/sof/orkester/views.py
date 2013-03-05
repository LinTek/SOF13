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

from django.db.models import Count, Q
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from forms import OrchestraForm, MemberForm, AddMemberForm
from models import Orchestra, Member, YES, TICKET_TYPES, GADGETS_TSHIRT


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


@login_required
def food_list(request):
    days = {'thursday': ('thursday',),
            'friday': ('thursday', 'friday'),
            'saturday': ('thursday', 'friday', 'saturday'),
            'sunday': ('thursday', 'friday')}

    for day in days:
        pass

    return render(request, 'orkester/food_list.html',
                  {'days': days})


@login_required
def stats(request):
    orchestras = (Orchestra.objects.order_by('orchestra_name')
                                   .select_related('member')
                                   .annotate(member_count=Count('member')))

    for orchestra in orchestras:
        members = orchestra.member_set.all()

        orchestra.totals = defaultdict(int)
        orchestra.totals['members'] = len(members)
        orchestra.totals['sitting'] = len([True for m in members if (m.attend_sitting == YES)])
        orchestra.totals['bed'] = len([True for m in members if (m.needs_bed == YES)])
        orchestra.totals['kartege'] = len([True for m in members if (m.plays_kartege == YES)])

        for member in members:
            orchestra.totals[member.ticket_type] += 1

        for gtype, _ in GADGETS_TSHIRT:
            # Python magic FTW!
            orchestra.totals[gtype] = members.filter(**{gtype: True}).count()

    # This is needed because we have no knowledge about members that belong to
    # multiple orchestras, so we cannot just sum all the stuff above.
    totals = {}
    totals['members'] = Member.objects.count()
    totals['sitting'] = Member.objects.filter(attend_sitting=YES).count()
    totals['bed'] = Member.objects.filter(needs_bed=YES).count()
    totals['kartege'] = Member.objects.filter(plays_kartege=YES).count()

    for ttype, _ in TICKET_TYPES:
        totals[ttype] = Member.objects.filter(ticket_type=ttype).count()

    for gtype, _ in GADGETS_TSHIRT:
        # Python magic FTW!
        totals[gtype] = Member.objects.filter(**{gtype: True}).count()

    return render(request, 'orkester/stats.html',
                  {'orchestras': orchestras,
                   'totals': totals,
                   'ticket_types': TICKET_TYPES,
                   'gadget_types': GADGETS_TSHIRT})


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
