from django.conf.urls import patterns, url

urlpatterns = patterns(
    'sof.tickets.views',

    url(r'^sell$', 'sell', name='ticket_sell'),
    url(r'^person/(?P<pk>\d+)/$', 'person_details', name='person_details')
)
