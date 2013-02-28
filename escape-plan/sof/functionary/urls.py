from django.conf.urls import patterns, url, include

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
from django.contrib.auth.views import logout

admin.autodiscover()

from .views import login


urlpatterns = patterns('sof.functionary.views',
    url(r'^$', login, {'template_name': 'functionary/login.html'}, 'login'),
    url(r'^logout$', logout, {'next_page': '/'}, 'logout'),
    url(r'^list/$', 'public_shift_list', name='public_shift_list'),

    url(r'^shifts$', 'shifts', name='shifts'),
    url(r'^search$', 'search', name='search'),
    url(r'^create-worker$', 'create_worker', name='create_worker'),

    url(r'^add-registration$', 'add_registration', name='add_registration'),
    url(r'^add-registrations/(?P<worker_id>\d+)$',
            'add_registrations', name='add_registrations'),

    url(r'^send-confirmation/(?P<worker_id>\d+)$', 'send_confirmation', name='send_confirmation'),

    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += staticfiles_urlpatterns()
