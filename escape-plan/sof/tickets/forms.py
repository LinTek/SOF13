from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import TicketType


class TurboTicketForm(forms.Form):
    ticket_type = forms.ModelChoiceField(queryset=TicketType.objects.active(),
                                         widget=forms.RadioSelect,
                                         required=True,
                                         empty_label=None)

    term = forms.CharField(label=_('LiU-ID or card number'),
                           max_length=20, required=True)
