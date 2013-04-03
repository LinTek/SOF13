from django.conf.urls import patterns, url

urlpatterns = patterns(
    'sof.invoices.views',

    url(r'^$', 'invoice_list', name='invoice_list'),
    url(r'^set-handed-out/(?P<pk>\d+)/$', 'set_handed_out', name='set_handed_out'),
)
