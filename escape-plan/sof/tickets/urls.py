from django.conf.urls import patterns, url

urlpatterns = patterns(
    'sof.tickets.views',

    url(r'^sell$', 'sell', name='ticket_sell'),
    url(r'^buy$', 'preemption', name='preemption'),

    url(r'^public$', 'public_sell', name='public_sell'),
    url(r'^public-non-liu$', 'public_non_liu_sell', name='public_non_liu_sell'),

    url(r'^confirm/(?P<token>\w+)/$', 'confirm', name='confirm'),
    url(r'^person/(?P<pk>\d+)/$', 'person_details', name='person_details'),

    url(r'^turbo-submit$', 'turbo_submit', name='turbo_submit'),
    url(r'^turbo-confirm$', 'turbo_confirm', name='turbo_confirm'),
)
