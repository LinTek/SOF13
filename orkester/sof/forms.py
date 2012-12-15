# encoding: utf-8
from django import forms

from orkester.models import Orchestra

TITLES = {
    'name': 'Orkester-information',
    'departure_day': 'Under SOF',
    'play_thursday': 'Spelningar',
    'backline': 'Extra utrustning',
    'primary_contact_name': 'Kontaktperson',
    'message': 'Övrigt',
}


class OrchestraForm(forms.ModelForm):
    class Meta:
        model = Orchestra

    def __init__(self):
        super(OrchestraForm, self).__init__()

        for k, v in TITLES.iteritems():
            self.fields[k].title = v
