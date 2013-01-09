"""
urls.py

This file maps urls to different views. When an url gets to this file, it has
already passed through the global conf/urls.py before it ended up here.

Urls are specified with a regex of the url, the name of the view it should
point to, and last a name which is used when redirecting or when rendering
urls in templates.
"""
from django.conf.urls import patterns, url

from sof.orkester.views import (confirm_orchestra, confirm_member, orchestra_form,
                                member_form, member_list, add_member, home)


urlpatterns = patterns('',
    url(r'^$', home, name='home'),

    url(r'^thanks/$', confirm_member, name='confirm_member'),
    url(r'^confirm/$', confirm_orchestra, name='confirm_orchestra'),
    url(r'^create/$', orchestra_form, name='orchestra_form'),

    url(r'^register/(?P<token>\w+)/$', member_form, name='member_form'),
    url(r'^register/(?P<token>\w+)/add/$', add_member, name='add_member'),

    url(r'^list/(?P<token>\w+)/$', member_list, name='member_list'),
)
