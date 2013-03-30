from django.conf.urls import patterns, url

from views import PersonDetailView

urlpatterns = patterns(
    'sof.tickets.views',

    url(r'^sell$', 'sell', name='ticket_sell'),

    url(r'^person/(?P<pk>\d+)/$',
        view=PersonDetailView.as_view(),
        name='person_details')
)
