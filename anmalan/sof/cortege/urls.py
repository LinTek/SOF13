from django.conf.urls import patterns, url, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
admin.autodiscover()

from .views import home, confirm_contribution

urlpatterns = patterns('',
    url(r'^$', home, name='home'),
    url(r'^admin/', include(admin.site.urls)),

    url(r'confirm/', confirm_contribution, name='confirm_contribution'),
)

urlpatterns += staticfiles_urlpatterns()
