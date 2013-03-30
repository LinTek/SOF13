import re

from django import forms
from django.core.exceptions import ValidationError

from django_localflavor_se.forms import SEPersonalIdentityNumberField
from django_localflavor_se.utils import (validate_id_birthday,
                                         format_personal_id_number)

FORGIVING_PID = re.compile(r'^(?P<century>\d{2})?(?P<year>\d{2})(?P<month>\d{2})(?P<day>\d{2})(?P<sign>[\-+])?(?P<serial>\w{4})$')


class ForgivingPIDField(SEPersonalIdentityNumberField):
    """
    A personal identification number field which also accepts some fake PID:s
    """
    def clean(self, value):
        try:
            value = super(ForgivingPIDField, self).clean(value)
        except forms.ValidationError as e:
            if value is None:
                raise forms.ValidationError(self.error_messages['required'])

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


def format_kobra_pid(value):
    value = value[2:]
    return "%s-%s" % (value[0:6], value[6:10])


def format_pid(value):
    from .forms import ForgivingPIDField

    try:
        return ForgivingPIDField().clean(value)
    except ValidationError:
        return None
