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
        # render every single field manually. Which is what we normally do, but
        # not when the number of fields almost goes to infinity as in this case...
        for k, v in TITLES.iteritems():
            self.fields[k].title = v

        self.fields['sof_count'].extra_text = """
            Berätta lite om er själva (dessa frågor kan komma att användas i
                SOF–tidningen)"""


class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        exclude = ('orchestras')

    # clean performs form validation of the whole form, after each field's
    # own clean-method has been called. This is used for validating stuff
    # that depends on each other.
    def clean(self):
        cd = super(MemberForm, self).clean()
        # if t-shirt is selected but no size chosen
        if cd.get('t_shirt', False) and not cd.get('t_shirt_size'):

            # We could justiraise ValidationError here, but we want the error
            # to be displayed at the t-shirt size field.
            self._errors['t_shirt_size'] = self.error_class(['Välj en storlek på t-shirt'])
            del cd['t_shirt_size']

        return cd

    # Override the standard charfield with a localflavor personnummer field
    # to get validation and stuff
    pid = SEPersonalIdentityNumberField(label='Personnummer')


class AddMemberForm(forms.Form):
    pid = SEPersonalIdentityNumberField(label='Personnummer')

    def clean_pid(self):
        pid = self.cleaned_data.get('pid')

        if not Member.objects.filter(pid=pid).exists():
            raise ValidationError('Det finns ingen registrerad person med detta personnummer.')

        return pid
