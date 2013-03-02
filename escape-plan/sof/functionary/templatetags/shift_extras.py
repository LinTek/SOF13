from django import template

register = template.Library()


@register.inclusion_tag('functionary/partials/shift_title.html')
def shift_title(shift, place_count=False, sub_type=False):
    return {'shift': shift, 'place_count': bool(place_count),
            'sub_type': bool(sub_type)}
