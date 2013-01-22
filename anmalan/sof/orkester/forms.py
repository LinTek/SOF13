# encoding: utf-8
"""
forms.py

Forms is Django's approach to handling - forms (surprisingly). Forms can
be generated from models to easily create a new instance of a model, and
is primarily responsible for validation of form input.
"""
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.localflavor.se.forms import SEPersonalIdentityNumberField

from models import Orchestra, Member


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
        exclude = ('orchestras')

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

        if cd.get('attends_10th_year') and cd.get('attends_25th_year'):
            raise ValidationError('I år kan inte vara både det 10:e och 25:e året du deltar i SOF.')

        return cd

    # Override the standard charfield with a localflavor personnummer field
    # to get validation and stuff
    pid = SEPersonalIdentityNumberField(label='Personnummer')


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
