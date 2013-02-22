from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import Worker


class SearchForm(forms.Form):
    term = forms.CharField(label=_('LiU-ID or card number'),
                           max_length=20, required=False)


class AddWorkerForm(forms.ModelForm):
    class Meta:
        model = Worker
        fields = ('first_name', 'last_name', 'liu_id', 'email')

    lintek = forms.BooleanField(label=_('LinTek member'))
