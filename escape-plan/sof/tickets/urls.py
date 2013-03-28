from django.conf.urls import patterns, url

urlpatterns = patterns(
    'sof.tickets.views',

    url(r'^search$', 'ticket_search', name='ticket_search'),
)
