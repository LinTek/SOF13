from sof.functionary.models import Shift

for r in Shift.objects.get(pk=1301).workerregistration_set.all():  # superfunkis
    r.worker.super_worker = True
    r.worker.save()
