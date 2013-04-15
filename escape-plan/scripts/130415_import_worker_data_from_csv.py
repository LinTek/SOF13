# encoding: utf-8
import csv

from sof.functionary.models import Worker

with open('workers.csv', 'rb') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        _, name, liu_id, phone, tshirt, ice, allergies, other = row
        liu_id = liu_id.lower().strip()

        if not liu_id:
            print "Missing LiU ID for %s" % name
            print row
            print
            continue

        try:
            worker = Worker.objects.get(liu_id=liu_id)

            if worker.has_meta_info:
                continue

            worker.has_meta_info = True
            worker.phone_number = phone
            worker.tshirt_size = tshirt
            worker.ice_number = ice
            worker.allergies = allergies
            worker.other = other
            worker.save()

        except Worker.DoesNotExist:
            print "Cound not find %s (%s)" % (name, liu_id)
            print row
            print
