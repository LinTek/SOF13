from django import template

register = template.Library()


@register.inclusion_tag('functionary/partials/shift_title.html')
def shift_title(shift, place_count=False, admin=False):
    return {'shift': shift, 'place_count': bool(place_count),
            'admin': bool(admin)}


@register.inclusion_tag('functionary/partials/check_in_status.html')
def check_in_status(registration):
    return {'r': registration}


@register.inclusion_tag('functionary/partials/info_meeting_status.html')
def info_meeting_status(worker):
    return {'worker': worker}


@register.inclusion_tag('functionary/partials/merchandise_status.html')
def merchandise_status(worker):
    return {'worker': worker}
