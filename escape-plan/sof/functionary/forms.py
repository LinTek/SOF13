import re

from django_localflavor_se.forms import SEPersonalIdentityNumberField
from django_localflavor_se.utils import (validate_id_birthday,
                                         format_personal_id_number)

from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import Worker

FORGIVING_PID = re.compile(r'^(?P<century>\d{2})?(?P<year>\d{2})(?P<month>\d{2})(?P<day>\d{2})(?P<sign>[\-+])?(?P<serial>\w{4})$')


class ForgivingPIDField(SEPersonalIdentityNumberField):
    """
    A personal identification number field which also accepts some fake PID:s
    """
    def clean(self, value):
        try:
            value = super(ForgivingPIDField, self).clean(value)
        except forms.ValidationError as e:
            match = FORGIVING_PID.match(value)
            if not match:
                raise e

            gd = match.groupdict()
            gd['checksum'] = ''

            # check for valid birthday
            try:
                birth_day = validate_id_birthday(gd, fix_coordination_number_day=False)
            except ValueError:
                raise forms.ValidationError(self.error_messages['invalid'])

            return format_personal_id_number(birth_day, gd)
        return value


class SearchForm(forms.Form):
    term = forms.CharField(label=_('LiU-ID or card number'),
                           max_length=20, required=False)


class AddWorkerForm(forms.ModelForm):
    class Meta:
        model = Worker
        fields = ('first_name', 'last_name', 'email', 'pid')

    lintek = forms.BooleanField(label=_('LinTek member'), required=False)
    pid = ForgivingPIDField(label=_('Personal identification number'))
