from django.conf.urls import patterns, url

urlpatterns = patterns(
    'sof.invoices.views',

    url(r'^$', 'invoice_list', name='invoice_list'),
    url(r'^stats$', 'stats', name='stats'),

    url(r'^set-handed-out-special/(?P<pk>\d+)/$',
        'set_handed_out_special', name='set_handed_out_special'),
    url(r'^set-handed-out/(?P<pk>\d+)/$', 'set_handed_out', name='set_handed_out'),
    url(r'^set-paid/(?P<pk>\d+)/$', 'set_paid', name='set_paid'),
    url(r'^send-email/(?P<pk>\d+)/$', 'send_email', name='send_email'),
    url(r'^add-trappan/(?P<pk>\d+)/$', 'add_trappan', name='add_trappan'),

    url(r'^send-email-special/(?P<pk>\d+)/$', 'send_email_special', name='send_email_special'),
)
