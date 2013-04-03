from django.conf.urls import patterns, url

urlpatterns = patterns(
    'sof.functionary.views',


    url(r'^shifts$', 'shifts', name='shifts'),
    url(r'^search$', 'search', name='functionary_search'),
    url(r'^create-worker$', 'create_worker', name='create_worker'),

    url(r'^add-registrations/(?P<worker_id>\d+)$', 'add_registrations',
        name='add_registrations'),
    url(r'^approve-contract/(?P<worker_id>\d+)$', 'approve_contract',
        name='approve_contract'),
    url(r'^add-registration$', 'add_registration',
        name='add_registration'),


    url(r'^send-confirmation/(?P<worker_id>\d+)$', 'send_confirmation',
        name='send_confirmation'),
)
