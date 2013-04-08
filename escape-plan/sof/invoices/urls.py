from django.conf.urls import patterns, url

urlpatterns = patterns(
    'sof.invoices.views',

    url(r'^$', 'invoice_list', name='invoice_list'),

    url(r'^set-handed-out/(?P<pk>\d+)/$', 'set_handed_out', name='set_handed_out'),
    url(r'^set-paid/(?P<pk>\d+)/$', 'set_paid', name='set_paid'),
    url(r'^add-trappan/(?P<pk>\d+)/$', 'add_trappan', name='add_trappan'),
)
