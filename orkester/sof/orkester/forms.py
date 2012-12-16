# encoding: utf-8
from django import forms

from sof.orkester.models import Orchestra, Member


class OrchestraForm(forms.ModelForm):
    class Meta:
        model = Orchestra
        exclude = ('token')

    def __init__(self, *args, **kwargs):
        TITLES = {
            'orchestra_name':       'Orkester-information',
            'departure_day':        'Under SOF',
            'play_thursday':        'Spelningar',
            'backline':             'Extra utrustning',
            'primary_contact_name': 'Kontaktpersoner',
            'message':              'Övrigt',
        }

        super(OrchestraForm, self).__init__(*args, **kwargs)

        for k, v in TITLES.iteritems():
            self.fields[k].title = v

        self.fields['sof_count'].extra_text = """Berätta lite om er själva
                      (dessa frågor kan komma att användas i SOF – tidningen)"""


class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        exclude = ('orchestra')
