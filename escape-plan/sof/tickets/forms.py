from django import forms
from django.utils.translation import ugettext_lazy as _
from django.forms.widgets import RadioSelect, CheckboxSelectMultiple

from sof.utils.forms import ForgivingPIDField
from sof.functionary.models import Visitor, Worker

from .models import TicketType


class TicketTypeForm(forms.Form):
    # ModelChoiceFields are slightly retarded and get even more retarded with
    # checbox widgets and Django crispy forms...
    def __init__(self, *args, **kwargs):
        super(TicketTypeForm, self).__init__(*args, **kwargs)

        ticket_types = TicketType.objects.active()
        self.fields['ticket_type'].choices = [(choice.pk, unicode(choice))
                                              for choice in ticket_types]

        if ticket_types:
            self.fields['ticket_type'].initial = ticket_types[0].pk

    ticket_type = forms.MultipleChoiceField(required=True,
                                            widget=CheckboxSelectMultiple,
                                            label=_('Ticket type'))


class PreemptionTicketTypeForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(PreemptionTicketTypeForm, self).__init__(*args, **kwargs)

        ticket_types = TicketType.objects.all()
        self.fields['ticket_type'].choices = [(choice.pk, unicode(choice))
                                              for choice in ticket_types]

    ticket_type = forms.ChoiceField(required=True,
                                    widget=RadioSelect,
                                    label=_('Ticket type'))


class LiuIDForm(forms.Form):
    liu_id = forms.CharField(label=_('LiU-ID'), max_length=10, required=True)


class TurboTicketForm(forms.Form):
    term = forms.CharField(label=_('LiU-ID or card number'),
                           max_length=20, required=True)


class SearchForm(forms.Form):
    q = forms.CharField(label=_('Search query'), max_length=20, required=True)


class VisitorForm(forms.ModelForm):
    class Meta:
        model = Visitor
        fields = ('first_name', 'last_name', 'pid', 'liu_id', 'email', 'lintek_member')

    pid = ForgivingPIDField(label=_('Personal identification number'))


class WorkerForm(forms.ModelForm):
    class Meta:
        model = Worker
        fields = ('first_name', 'last_name', 'pid', 'liu_id', 'email', 'lintek_member')

    pid = ForgivingPIDField(label=_('Personal identification number'))
