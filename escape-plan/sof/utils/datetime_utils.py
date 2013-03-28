from pytz import timezone

from django.utils.dateformat import format


sthlm = timezone('Europe/Stockholm')


def format_dt(dt):
    return format(dt.astimezone(sthlm), 'l d F H:i')


def format_time(dt):
    return format(dt.astimezone(sthlm), 'H:i')
