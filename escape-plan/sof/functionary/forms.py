from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import Functionary


class SearchForm(forms.Form):
    term = forms.CharField(label=_('LiU-ID or card number'),
                           max_length=20, required=False)


class AddFunctionaryForm(forms.ModelForm):
    class Meta:
        model = Functionary
        fields = ('first_name', 'last_name', 'liu_id', 'email')
    lintek = forms.BooleanField(label=_('LinTek member'))
