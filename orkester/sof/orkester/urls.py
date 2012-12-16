from django.conf.urls import patterns, url


urlpatterns = patterns('',
    url(r'^$', 'sof.orkester.views.home', name='home'),

    url(r'^thanks/$', 'sof.orkester.views.confirm_member', name='confirm_member'),
    url(r'^confirm/$', 'sof.orkester.views.confirm_orchestra', name='confirm_orchestra'),
    url(r'^create/$', 'sof.orkester.views.orchestra_form', name='orchestra_form'),

    url(r'^register/(?P<token>\w+)/$', 'sof.orkester.views.member_form', name='member_form'),
    url(r'^register/(?P<token>\w+)/add/$', 'sof.orkester.views.add_member', name='add_member'),

)
