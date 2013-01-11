from django import template

from sof.orkester.models import boolify

register = template.Library()


@register.filter(name='boolify')
def _boolify(x):
    return boolify(x)
