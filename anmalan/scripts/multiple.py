#encoding: utf-8
from django.db.models import Count
from sof.orkester.models import Orchestra, Member

for member in Member.objects.annotate(c=Count('orchestras')).filter(c__gt=1).order_by('first_name'):
    print(unicode(member))
    print(', '.join([o.orchestra_name for o in member.orchestras.order_by('id')]))
    print(member.get_gadgets_display())
    print('---------------')
