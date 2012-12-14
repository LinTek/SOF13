from django import forms

from orkester.models import Orchestra

class OrchestraForm(forms.ModelForm):
    class Meta:
        model = Orchestra
