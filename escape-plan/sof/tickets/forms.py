from django import forms
from django.utils.translation import ugettext_lazy as _
from django.forms.widgets import CheckboxSelectMultiple

from sof.utils.forms import ForgivingPIDField
from sof.functionary.models import Visitor, Worker

from .models import TicketType


class TicketTypeForm(forms.Form):
    # ModelChoiceFields are slightly retarded and get even more retarded with
    # checbox widgets and Django crispy forms...
    def __init__(self, *args, **kwargs):
        display_all = False

        if 'display_all' in kwargs:
            display_all = kwargs.pop('display_all')

        super(TicketTypeForm, self).__init__(*args, **kwargs)

        if display_all:
            ticket_types = TicketType.objects.all()
        else:
            ticket_types = TicketType.objects.active()

        self.fields['ticket_type'].choices = [(choice.pk, unicode(choice))
                                              for choice in ticket_types]

        if ticket_types:
            self.fields['ticket_type'].initial = ticket_types[0].pk

    ticket_type = forms.MultipleChoiceField(required=True,
                                            widget=CheckboxSelectMultiple,
                                            label=_('Ticket type'))

    def clean(self):
        c = self.cleaned_data['ticket_type']
        # Officially the ugliest thing I've ever done. Tokfulhaxx!
        if '1' in c:
            if '11' in c or '21' in c or '31' in c:
                raise forms.ValidationError(_('Conflicting ticket types'))
        return self.cleaned_data


class PreemptionTicketTypeForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(PreemptionTicketTypeForm, self).__init__(*args, **kwargs)

        ticket_types = TicketType.objects.all()
        self.fields['ticket_type'].choices = [(choice.pk, unicode(choice))
                                              for choice in ticket_types]

    ticket_type = forms.MultipleChoiceField(required=True,
                                            widget=CheckboxSelectMultiple,
                                            label=_('Ticket type'))

    def clean(self):
        cleaned_data = super(PreemptionTicketTypeForm, self).clean()
        c = cleaned_data.get('ticket_type')
        # Officially the ugliest thing I've ever done. Tokfulhaxx!
        if c and '1' in c:
            if '11' in c or '21' in c or '31' in c:
                raise forms.ValidationError(_('Conflicting ticket types'))
        return self.cleaned_data


# Copypaste FTW.....
class PublicTicketTypeForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(PublicTicketTypeForm, self).__init__(*args, **kwargs)

        ticket_types = TicketType.objects.public()
        self.fields['ticket_type'].choices = [(choice.pk, unicode(choice))
                                              for choice in ticket_types]

    ticket_type = forms.MultipleChoiceField(required=True,
                                            widget=CheckboxSelectMultiple,
                                            label=_('Ticket type'))

    def clean(self):
        cleaned_data = super(PublicTicketTypeForm, self).clean()
        c = cleaned_data.get('ticket_type')
        # Officially the ugliest thing I've ever done. Tokfulhaxx!
        if c and '1' in c:
            if '11' in c or '21' in c or '31' in c:
                raise forms.ValidationError(_('Conflicting ticket types'))
        return self.cleaned_data


class LiuIDForm(forms.Form):
    liu_id = forms.CharField(label=_('LiU-ID or PID'), max_length=10, required=True)


class TurboTicketForm(forms.Form):
    term = forms.CharField(label=_('LiU-ID or card number'),
                           max_length=20, required=True)


class SearchForm(forms.Form):
    q = forms.CharField(label=_('Search query'), max_length=20, required=True)


class VisitorForm(forms.ModelForm):
    class Meta:
        model = Visitor
        fields = ('first_name', 'last_name', 'pid', 'email', 'lintek_member',
                  'rfid_number', 'barcode_number', 'liu_id')
        widgets = {
            'rfid_number': forms.widgets.HiddenInput(),
            'barcode_number': forms.widgets.HiddenInput(),
            'liu_id': forms.widgets.HiddenInput(),
        }

    pid = ForgivingPIDField(label=_('Personal identification number'))


class WorkerForm(forms.ModelForm):
    class Meta:
        model = Worker
        fields = ('first_name', 'last_name', 'pid', 'email', 'lintek_member',
                  'rfid_number', 'barcode_number', 'liu_id')
        widgets = {
            'rfid_number': forms.widgets.HiddenInput(),
            'barcode_number': forms.widgets.HiddenInput(),
            'liu_id': forms.widgets.HiddenInput(),
        }

    pid = ForgivingPIDField(label=_('Personal identification number'))
