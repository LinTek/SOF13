from django.conf.urls import patterns, url, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'sof.orkester.views.home', name='home'),
    url(r'^thanks/$', 'sof.orkester.views.confirm_member', name='confirm_member'),
    url(r'^confirm/$', 'sof.orkester.views.confirm_orchestra', name='confirm_orchestra'),

    url(r'^create_orchestra/$', 'sof.orkester.views.orchestra_form', name='orchestra_form'),
    url(r'^register/(?P<token>\w+)/$', 'sof.orkester.views.member_form', name='member_form'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += staticfiles_urlpatterns()
