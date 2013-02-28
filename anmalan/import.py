# encoding: utf-8
import csv

from sof.orkester.models import Orchestra, Member, YES, NO


TECHNIQUE_INFRIENDLY_ORCHESTRA = Orchestra.objects.get(pk=241)

with open('orkester.csv', 'rb') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        fname, lname, pid, email, _, tenth, _, _, allergy = row[:9]

        member = Member(first_name=unicode(fname, 'utf-8'),
                        last_name=unicode(lname, 'utf-8'),
                        pid='19%s' % pid.replace('-', ''),
                        email=email,
                        ticket_type='friday',
                        attends_10th_year=(tenth == 'x'),
                        attends_25th_time=False,
                        plays_kartege=YES,
                        allergies=unicode(allergy, 'utf-8'),
                        needs_bed=YES,
                        attend_sitting=NO,
                        badge_orchestra=True,
                        medal=True)
        member.save()
        member.orchestras.add(TECHNIQUE_INFRIENDLY_ORCHESTRA)

        print member
