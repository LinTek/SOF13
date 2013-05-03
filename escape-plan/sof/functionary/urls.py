from django.conf.urls import patterns, url

urlpatterns = patterns(
    'sof.functionary.views',


    url(r'^shifts$', 'shifts', name='shifts'),
    url(r'^search$', 'search', name='search'),
    url(r'^create-worker$', 'create_worker', name='create_worker'),
    url(r'^list-workers$', 'list_workers', name='list_workers'),
    url(r'^workers-by-type$', 'workers_by_type', name='workers_by_type'),
    url(r'^worker-check-in/(?P<date>[-\d]+)?$', 'worker_check_in', name='worker_check_in'),

    url(r'^toggle-checked-in/$', 'toggle_checked_in', name='toggle_checked_in'),
    url(r'^toggle-checked-out/$', 'toggle_checked_out', name='toggle_checked_out'),
    url(r'^toggle-info-meeting/$', 'toggle_info_meeting', name='toggle_info_meeting'),
    url(r'^toggle-merchandise/$', 'toggle_merchandise', name='toggle_merchandise'),

    url(r'^add-registrations/(?P<worker_id>\d+)$', 'add_registrations',
        name='add_registrations'),
    url(r'^approve-contract/(?P<worker_id>\d+)$', 'approve_contract',
        name='approve_contract'),
    url(r'^add-registration$', 'add_registration',
        name='add_registration'),


    url(r'^send-confirmation/(?P<worker_id>\d+)$', 'send_confirmation',
        name='send_confirmation'),
)
