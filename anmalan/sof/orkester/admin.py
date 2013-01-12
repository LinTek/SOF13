"""
admin.py

This just makes sure that the models show up in the admin interface at /admin.
If you want to add new model classes, you probably want to add them here.
"""
from django.contrib import admin

from sof.orkester.models import Orchestra, Member

admin.site.register(Orchestra)
admin.site.register(Member)
