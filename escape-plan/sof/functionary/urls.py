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

    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += staticfiles_urlpatterns()
