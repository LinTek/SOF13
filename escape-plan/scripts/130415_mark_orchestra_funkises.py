from sof.functionary.models import Shift

for r in Shift.objects.get(pk=1311).workerregistration_set.all():  # orkesterfadder
    r.worker.orchestra_worker = True
    r.worker.save()
