from django.conf.urls import patterns, url, include

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
from django.contrib.auth.views import logout

admin.autodiscover()

from .views import login


urlpatterns = patterns('sof.functionary.views',
    url(r'^$', login, {'template_name': 'functionary/login.html'}, 'login'),
    url(r'^logout$', logout, {'next_page': '/'}, 'logout'),

    url(r'^shifts$', 'shifts', name='shifts'),
    url(r'^search$', 'search', name='search'),
    url(r'^add_worker$', 'add_worker', name='add_worker'),
    url(r'^register_worker$', 'register_worker', name='register_worker'),
    url(r'^add_registrations/(?P<worker_id>\d+)$',
        'add_registrations', name='add_registrations'),

    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += staticfiles_urlpatterns()
