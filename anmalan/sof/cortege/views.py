from datetime import datetime

from django.shortcuts import render, redirect

from .forms import CortegeContributionForm

OPENING_DATE = datetime(2013, 1, 14, 12, 0)
CLOSING_DATE = datetime(2013, 2, 1, 12, 0)


def home(request):
    now = datetime.now()

    if now < OPENING_DATE or now > CLOSING_DATE:
        if not request.user.is_authenticated():
            return render(request, 'cortege/closed.html')

    form = CortegeContributionForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('confirm_contribution')

    return render(request, 'cortege/cortege_form.html', {'form': form})


def confirm_contribution(request):
    return render(request, 'cortege/confirm.html')
