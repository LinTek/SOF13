from django import template

from sof.orkester.models import boolify, Orchestra

register = template.Library()


@register.filter(name='boolify')
def _boolify(x):
    return boolify(x)


@register.filter(name='verbose_name')
def _verbose_name(field):
    return Orchestra._meta.get_field(field).verbose_name


@register.filter(name='getattr')
def _getattr(obj, name):
    return getattr(obj, name)
