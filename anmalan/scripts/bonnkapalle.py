from sof.orkester.models import Orchestra

bk = Orchestra.objects.get(pk=121)

for member in bk.member_set.all():
    member.ticket_type = 'saturday'
    member.save()
