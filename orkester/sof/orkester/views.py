from django.shortcuts import render, redirect, get_object_or_404

from forms import OrchestraForm, MemberForm, AddMemberForm
from models import Orchestra, Member


def home(request):
    return render(request, 'index.html')


def confirm_member(request):
    return render(request, 'orkester/confirm_member.html')


def confirm_orchestra(request):
    return render(request, 'orkester/confirm_orchestra.html')


def orchestra_form(request):
    if request.method == 'POST':
        form = OrchestraForm(request.POST, request.FILES)

        if form.is_valid():
            orchestra = form.save(commit=False)
            orchestra.generate_token()
            orchestra.save()
            orchestra.send_confirm_email()

            return redirect('confirm_orchestra')
    else:
        form = OrchestraForm()

    return render(request, 'orkester/orchestra_form.html', {'form': form})


def member_form(request, token):
    orchestra = get_object_or_404(Orchestra, token=token)

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


def add_member(request, token):
    orchestra = get_object_or_404(Orchestra, token=token)

    if request.method == 'POST':
        form = AddMemberForm(request.POST)

        if form.is_valid():
            pid = form.cleaned_data.get('pid')
            member = Member.objects.get(pid=pid)
            member.orchestras.add(orchestra)

            member.send_confirm_email(orchestra)

            return redirect('confirm_member')
    else:
        form = AddMemberForm()

    return render(request, 'orkester/add_member_form.html',
                    {'form': form, 'orchestra': orchestra})
