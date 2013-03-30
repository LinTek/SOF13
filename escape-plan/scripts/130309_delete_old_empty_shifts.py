# encoding: utf-8
from sof.functionary.models import Shift

for shift in Shift.objects.all():
    if shift.is_dummy:
        continue

    reg_count = shift.workerregistration_set.count()

    if reg_count == 0:
        shift.delete()
    else:
        shift.max_workers = reg_count
        shift.save()
