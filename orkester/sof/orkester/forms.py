# encoding: utf-8
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.localflavor.se.forms import SEPersonalIdentityNumberField

from models import Orchestra, Member


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

        # This is ugly and hackish, but made since we otherwise would have to
        # render every single field manually...
        for k, v in TITLES.iteritems():
            self.fields[k].title = v

        self.fields['sof_count'].extra_text = """
            Berätta lite om er själva (dessa frågor kan komma att användas i
                SOF–tidningen)"""

        self.fields['play_length'].extra_text = """Under lördagen kommer det
            enbart att finnas möjlighet att spela en gång på området utöver
            Conserto Grosso (exklusive stadsspelningarna)"""


class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        exclude = ('orchestras')

    pid = SEPersonalIdentityNumberField(label='Personnummer')


class AddMemberForm(forms.Form):
    pid = SEPersonalIdentityNumberField(label='Personnummer')

    def clean_pid(self):
        pid = self.cleaned_data.get('pid')

        if not Member.objects.filter(pid=pid).exists():
            raise ValidationError('Det finns ingen registrerad person med detta personnummer.')

        return pid
