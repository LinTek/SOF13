from django.conf.urls import patterns, url, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
from django.contrib.auth.views import logout

admin.autodiscover()

from sof.functionary.views import login, public_shift_list


urlpatterns = patterns(
    '',

    url(r'^$', login, {'template_name': 'login.html'}, 'login'),
    url(r'^logout$', logout, {'next_page': '/'}, 'logout'),

    url(r'^list', public_shift_list, name='public_shift_list'),

    url(r'^funktionar/', include('sof.functionary.urls')),
    url(r'^tickets/', include('sof.tickets.urls')),
    url(r'^invoices/', include('sof.invoices.urls')),

    url(r'^admin/', include(admin.site.urls)),
)


urlpatterns += staticfiles_urlpatterns()
