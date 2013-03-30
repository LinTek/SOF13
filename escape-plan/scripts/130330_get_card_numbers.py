from django.conf import settings

from sof.functionary.models import Worker
from sof.utils.forms import format_kobra_pid
from sof.utils.kobra_client import KOBRAClient, StudentNotFound

client = KOBRAClient(settings.KOBRA_USER, settings.KOBRA_KEY)

for worker in Worker.objects.order_by('first_name', 'last_name'):
    print worker.get_full_name()

    try:
        student = client.get_student_by_pid(format_kobra_pid(worker.pid))

        worker.lintek_member = (student.get('union') == 'LinTek')
        worker.liu_id = student.get('liu_id')
        worker.rfid_number = student.get('rfid_number')
        worker.barcode_number = student.get('barcode_number')
        worker.save()

    except StudentNotFound:
        print '  !!! Not found'
