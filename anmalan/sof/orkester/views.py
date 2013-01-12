# encoding: utf-8
"""
views.py

A view is called when a visited url-entry in urls.py points to it.
They must return a HTTPResponse-object, which often is a rendered view or
redirect. Views typically creates and saves form instances, fetches stuff
from database or calls methods on models. Be careful not to do too much
work in the views to maintain a somewhat good MVC-pattern.
"""
from django.shortcuts import render, redirect, get_object_or_404

from forms import OrchestraForm, MemberForm, AddMemberForm
from models import Orchestra, Member


def home(request):
    return render(request, 'orkester/index.html')


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
    members = orchestra.member_set.all()

    return render(request, 'orkester/member_list.html',
                    {'orchestra': orchestra, 'members': members})


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
    Helper function which just fetches an orchestra from a token or returns
    HTTP 404 is not found.
    """
    return get_object_or_404(Orchestra, token=token)
