from django.shortcuts import render, redirect

from forms import OrchestraForm


def home(request):
    return render(request, 'index.html')


def orchestra_form(request):
    if request.method == 'POST':
        form = OrchestraForm(request.POST)
        if form.is_valid():
            return redirect('/')
    else:
        form = OrchestraForm()

    return render(request, 'orkester/orchestra_form.html', {
        'form': form,
    })
