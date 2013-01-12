from django.conf.urls import patterns, url

from .views import home, confirm_contribution

urlpatterns = patterns('',
    url(r'^$', home, name='home'),
    url(r'confirm/', confirm_contribution, name='confirm_contribution'),
)
