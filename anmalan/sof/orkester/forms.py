# encoding: utf-8
"""
forms.py

Forms is Django's approach to handling - forms (surprisingly). Forms can
be generated from models to easily create a new instance of a model, and
is primarily responsible for validation of form input.
"""
import re

from django import forms
from django.core.exceptions import ValidationError
from django.contrib.localflavor.se.forms import SEPersonalIdentityNumberField
from django.contrib.localflavor.se.utils import (validate_id_birthday,
                                                 format_personal_id_number)

from models import Orchestra, Member

SWEDISH_BIRTH_DATE = re.compile(r'^(?P<century>\d{2})?(?P<year>\d{2})(?P<month>\d{2})(?P<day>\d{2})$')


class BirthDateField(SEPersonalIdentityNumberField):
    def clean(self, value):
        try:
            value = super(BirthDateField, self).clean(value)
        except forms.ValidationError as e:
            match = SWEDISH_BIRTH_DATE.match(value)
            if not match:
                raise e

            gd = match.groupdict()
            gd['sign'] = gd['serial'] = gd['checksum'] = ''

            # check for valid birthday
            try:
                birth_day = validate_id_birthday(gd, fix_coordination_number_day=False)
            except ValueError:
                raise forms.ValidationError(self.error_messages['invalid'])

            return format_personal_id_number(birth_day, gd)
        return value


class OrchestraForm(forms.ModelForm):
    """
    This form is used to create new Orchestras. It is fully generated from
    the model.
    """
    class Meta:
        model = Orchestra  # tell ModelForm which model to use
        exclude = ('token')  # do not let the orchestras pick their token...

    # The stuff below is ugly and hackish, but done since we otherwise would
    # have to render every single field manually. Which is what we normally do,
    # but not when the number of fields almost goes to infinity as in this case...
    def __init__(self, *args, **kwargs):
        TITLES = {
            'orchestra_name':       'Orkester-information',
            'departure_day':        'Under SOF',
            'play_thursday':        'Spelningar',
            'backline':             'Extra utrustning',
            'primary_contact_name': 'Kontaktpersoner',
            'message':              'Övrigt',
        }

        # Anyways, this just sets titles-properties to fields
        super(OrchestraForm, self).__init__(*args, **kwargs)

        for k, v in TITLES.iteritems():
            self.fields[k].title = v

        self.fields['sof_count'].extra_text = """
            Berätta lite om er själva (dessa frågor kan komma att användas i
                SOF–tidningen)"""


class MemberForm(forms.ModelForm):
    """
    This form is used for adding new people to an Orchestra. It is pretty
    straightforward and mostly generated from the model.

    We also need to do some manual validation and overriding of a field.
    """
    class Meta:
        model = Member
        exclude = ('orchestras', 'late_registration')

    def clean(self):
        """
        Validates that t-shirt size is given if t-shirt is ordered.
        """
        # make sure the ModelForm's clean method is called
        cd = super(MemberForm, self).clean()

        # if t-shirt is selected but no size chosen
        if cd.get('t_shirt', False) and not cd.get('t_shirt_size'):

            # We could just raise ValidationError here, but we want the error
            # to be displayed at the t-shirt size field.
            self._errors['t_shirt_size'] = self.error_class(['Välj en storlek på t-shirt'])
            del cd['t_shirt_size']

        return cd

    accept = forms.BooleanField(required=True, label='Jag godkänner att SOF2013 lagrar mina uppgifter fram tills efter dess att festivalen genomförts')
    pid = BirthDateField(label='Personnummer')


class AddMemberForm(forms.Form):
    """
    This form is used when adding an existing member to an Orchestra.

    It is a normal, non-model Form, and just contains a pid. It validates
    that a Member with the entered pid exists in the database.
    """
    pid = SEPersonalIdentityNumberField(label='Personnummer')

    def clean_pid(self):
        pid = self.cleaned_data.get('pid')

        if not Member.objects.filter(pid=pid).exists():
            raise ValidationError('Det finns ingen registrerad person med detta personnummer.')

        return pid


class SearchForm(forms.Form):
    q = forms.CharField(max_length=40, label='Sökterm')
