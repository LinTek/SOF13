from django import forms

from .models import Functionary


class NewFunctionaryForm(forms.ModelForm):
    class Meta:
        model = Functionary
        fields = ('liu_card_number', 'liu_id', 'email')

class AddFunctionaryForm
