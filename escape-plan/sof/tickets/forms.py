from django import forms
from django.utils.translation import ugettext_lazy as _
from django.forms.widgets import CheckboxSelectMultiple

from sof.utils.forms import ForgivingPIDField

from .models import TicketType, Visitor


class TicketTypeForm(forms.Form):
    # ModelChoiceFields are slightly retarded and get even more retarded with
    # checbox widgets and Django crispy forms...
    def __init__(self, *args, **kwargs):
        super(TicketTypeForm, self).__init__(*args, **kwargs)
        self.fields['ticket_type'].choices = [(choice.pk, unicode(choice))
                                              for choice in TicketType.objects.active()]

    ticket_type = forms.MultipleChoiceField(required=True,
                                            widget=CheckboxSelectMultiple)


class TurboTicketForm(forms.Form):
    term = forms.CharField(label=_('LiU-ID or card number'),
                           max_length=20, required=True)


class SearchForm(forms.Form):
    q = forms.CharField(label=_('Search query'), max_length=20, required=True)


class VisitorForm(forms.ModelForm):
    class Meta:
        model = Visitor
        fields = ('first_name', 'last_name', 'email', 'pid')

    pid = ForgivingPIDField(label=_('Personal identification number'))
