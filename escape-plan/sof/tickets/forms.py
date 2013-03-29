from django import forms
from django.utils.translation import ugettext_lazy as _

from sof.utils.forms import ForgivingPIDField

from .models import TicketType, Visitor


class TicketTypeForm(forms.Form):
    ticket_type = forms.ModelChoiceField(queryset=TicketType.objects.active(),
                                         widget=forms.RadioSelect,
                                         required=True,
                                         empty_label=None)


class TurboTicketForm(forms.Form):
    term = forms.CharField(label=_('LiU-ID or card number'),
                           max_length=20, required=True)


class VisitorForm(forms.ModelForm):
    class Meta:
        model = Visitor
        fields = ('first_name', 'last_name', 'email', 'pid')

    pid = ForgivingPIDField(label=_('Personal identification number'))
