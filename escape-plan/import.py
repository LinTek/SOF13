# encoding: utf-8
import datetime
from pytz import timezone
from sof.functionary.models import Shift, ShiftSubType

sthlm = timezone('Europe/Stockholm')

types = {
    'super': 111,
    'flagg': 101,
    'event': 91,
    'logi': 81,
    'instrument': 71,
    'scen': 61,
    'säk': 51,
    'orkester': 41,
    'kårtege': 31,
    'servering': 21,
    'bygg': 11,
    'insats': 1,
}


with open('pass.txt') as f:
    date = None
    res = []

    for line in f:
        subtype = None

        if line == '\n':
            continue

        elif line[0].isdigit():
            date = datetime.datetime.strptime(line[0:-1], '%d/%m')
            date = date.replace(year=2013)
        else:
            line = line.replace('\n', '')
            t, startstop, workers, subtype = line.split(' ')

            if not subtype == '-':
                try:
                    subtype = ShiftSubType.objects.get(name=subtype)

                except ShiftSubType.DoesNotExist:
                    subtype = ShiftSubType(name=subtype).save()
            else:
                subtype = None

            start, stop = startstop.split('-')
            starttime = datetime.datetime.strptime(start, '%H.%M')
            stoptime = datetime.datetime.strptime(stop, '%H.%M')

            enddate = datetime.datetime.combine(
                date + datetime.timedelta(days=1 if stoptime < starttime else 0),
                stoptime.time())

            s = Shift(shift_type_id=types[t],
                      start=sthlm.localize(datetime.datetime.combine(date, starttime.time())),
                      end=sthlm.localize(enddate),
                      max_workers=int(workers), shift_sub_type=subtype)
            s.save()
            res.append(s)

for r in res:
    print r
