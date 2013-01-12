# encoding: utf-8
from django import forms
from django.core.exceptions import ValidationError

from .models import CortegeContribution


class CortegeContributionForm(forms.ModelForm):
    """
    This form is used for adding new people to an Orchestra. It is pretty
    straightforward and mostly generated from the model.

    We also need to do some manual validation and overriding of a field.
    """
    class Meta:
        model = CortegeContribution
        widgets = {
            'size_type': forms.RadioSelect,
        }

    needs_generator = forms.TypedChoiceField(coerce=lambda x: bool(int(x)),
                                      choices=((0, 'Ja'), (1, 'Nej')),
                                      label='Behöver elverk',
                                      widget=forms.RadioSelect)

    def clean(self):
        cd = super(CortegeContributionForm, self).clean()

        if cd.get('tickets_count') > cd.get('participant_count'):
            raise ValidationError('Antal biljetter får inte vara större än antalet deltagare.')
        return cd
