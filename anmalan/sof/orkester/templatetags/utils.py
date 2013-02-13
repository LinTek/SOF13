from django import template

from sof.orkester.models import boolify, Orchestra

register = template.Library()


@register.filter(name='boolify')
def _boolify(x):
    return boolify(x)


@register.filter(name='verbose_name')
def _verbose_name(field):
    return Orchestra._meta.get_field(field).verbose_name


@register.filter(name='get')
def _get(dic, name):
    return dic.get(name)


@register.filter(name='getattr')
def _getattr(obj, name):
    display_attr = 'get_%s_display' % name

    # if a display-attribute (for choice fields) is available, use that
    if hasattr(obj, display_attr):
        # since the display-attribute is a function, we need to call it
        return getattr(obj, display_attr)()

    return getattr(obj, name)
