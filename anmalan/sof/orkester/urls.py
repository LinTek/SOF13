"""
urls.py

This file maps urls to different views. When an url gets to this file, it has
already passed through the global conf/urls.py before it ended up here.

Urls are specified with a regex of the url, the name of the view it should
point to, and last a name which is used when redirecting or when rendering
urls in templates.
"""
from django.conf.urls import patterns, url, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
from django.contrib.auth.views import login, logout

admin.autodiscover()

urlpatterns = patterns(
    'sof.orkester.views',

    url(r'^$', 'home', name='home'),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^thanks/$', 'confirm_member', name='confirm_member'),
    url(r'^confirm/$', 'confirm_orchestra', name='confirm_orchestra'),
    url(r'^create/$', 'orchestra_form', name='orchestra_form'),  # backwards compability

    url(r'^check-in/$', 'check_in', name='check_in'),
    url(r'^toggle-handed-out/$', 'toggle_handed_out', name='toggle_handed_out'),
    url(r'^check-in/(?P<token>\w+)/$', 'check_in_list', name='check_in_list'),
    url(r'^check-in/(?P<token>\w+)/(?P<member_pk>\d+)$', 'check_in_list', name='check_in_list'),
    url(r'^set-all-handed-out/(?P<token>\w+)$', 'set_all_handed_out', name='set_all_handed_out'),

    url(r'^register/(?P<token>\w+)/$', 'member_form', name='member_form'),
    url(r'^register/(?P<token>\w+)/add/$', 'add_member', name='add_member'),

    url(r'^stats/$', 'stats', name='statistics'),
    url(r'^gadgets/$', 'gadgets', name='gadgets'),
    url(r'^sitting/(?P<sitting>\w+)?$', 'sitting_list', name='sitting'),
    url(r'^press/$', 'press_list', name='press'),
    url(r'^food/(?P<day>\w+)?$', 'food_list', name='food'),

    url(r'^list/$', 'orchestra_list', name='orchestra_list'),
    url(r'^list/(?P<token>\w+)/$', 'member_list', name='member_list'),

    url(r'^login$', login, {'template_name': 'login.html'}, 'login'),
    url(r'^logout$', logout, {'next_page': '/'}, 'logout'),

    url(r'^admin-home$', 'admin_home', name='admin_home'),
    url(r'^closed$', 'closed', name='closed'),
)

# Serve static and media files when using development server
urlpatterns += staticfiles_urlpatterns()
