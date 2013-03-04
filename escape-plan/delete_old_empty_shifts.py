# encoding: utf-8
from sof.functionary.models import Shift, ShiftSubType

for shift in Shift.objects.all():
    reg_count = shift.workerregistration_set.count()

    if reg_count == 0:
        shift.delete()
    else:
        shift.max_workers = reg_count
        shift.save()
