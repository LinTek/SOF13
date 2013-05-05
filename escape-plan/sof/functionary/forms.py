from django import forms
from django.utils.translation import ugettext_lazy as _

from sof.utils.forms import ForgivingPIDField

from .models import Worker


class SearchForm(forms.Form):
    term = forms.CharField(label=_('LiU-ID or card number'),
                           max_length=20, required=False)


class AddWorkerForm(forms.ModelForm):
    class Meta:
        model = Worker
        fields = ('first_name', 'last_name', 'email', 'pid')

    lintek = forms.BooleanField(label=_('LinTek member'), required=False)
    pid = ForgivingPIDField(label=_('Personal identification number'))


class NoteForm(forms.ModelForm):
    class Meta:
        model = Worker
        fields = ('other',)
