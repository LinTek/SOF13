# encoding: utf-8
from django import forms

from .models import CortegeContribution, SIZE_TYPES


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
                                      label='Behöver elverk (600 kr)',
                                      widget=forms.RadioSelect)

    def clean(self):
        cd = super(CortegeContributionForm, self).clean()

        if cd.get('tickets_count') > cd.get('participant_count'):
            # Again, we use this quite ugly code since raising ValidationError
            # would give an error on the whole form inseted of on the field.
            self._errors['tickets_count'] = self.error_class(['Antal biljetter får inte vara större än antalet deltagare.'])
            del cd['tickets_count']

        if cd.get('size_type'):
            if cd.get('participant_count') > SIZE_TYPES[cd.get('size_type')].max_count:
                self._errors['participant_count'] = self.error_class(['Du har angett fler deltagare än tillåtet för denna typ av bygge.'])
                del cd['participant_count']

        return cd
