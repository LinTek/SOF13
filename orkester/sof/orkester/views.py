import os

from django.shortcuts import render, redirect, get_object_or_404

from forms import OrchestraForm, MemberForm
from models import Orchestra


def home(request):
    return render(request, 'index.html')


def e500(request):
    assert False


def confirm_member(request):
    return render(request, 'orkester/confirm_member.html')


def confirm_orchestra(request):
    return render(request, 'orkester/confirm_orchestra.html')


def orchestra_form(request):
    if request.method == 'POST':
        form = OrchestraForm(request.POST, request.FILES)
        if form.is_valid():
            o = form.save(commit=False)
            o.token = os.urandom(10).encode('hex')
            o.save()

            #send_mail('Subject here', 'Wiee: ' + o.token, 'it@sof13.se', ['n@niclasolofsson.se'])

            return redirect('confirm_orchestra')
    else:
        form = OrchestraForm()

    return render(request, 'orkester/orchestra_form.html', {'form': form})


def member_form(request, token):
    orchestra = get_object_or_404(Orchestra, token=token)

    if request.method == 'POST':
        form = MemberForm(request.POST)

        if form.is_valid():
            member = form.save(commit=False)
            member.orchestra = orchestra
            member.save()

            return redirect('confirm_member')
    else:
        form = MemberForm()

    return render(request, 'orkester/member_form.html', {'form': form})
