# encoding: utf-8
from django.contrib import admin

from .models import (ShiftType, ShiftSubType, Shift, Worker, WorkerRegistration,
                     Person, Visitor)


class PersonAdmin(admin.ModelAdmin):
    list_select_related = True
    list_display = ('get_full_name', 'email')
    search_fields = ('first_name', 'last_name', 'email')


class WorkerRegistrationAdmin(admin.ModelAdmin):
    list_select_related = True
    list_display = ('worker', 'shift')
    search_fields = ('worker__first_name', 'worker__last_name', 'worker__email')


class ShiftAdmin(admin.ModelAdmin):
    list_select_related = True
    list_display = ('shift_type', 'shift_sub_type',
                    'start', 'end', 'max_workers')
    search_fields = ('shift_type__name', 'shift_sub_type__name')


admin.site.register(Person, PersonAdmin)
admin.site.register(Visitor, PersonAdmin)
admin.site.register(Worker, PersonAdmin)
admin.site.register(WorkerRegistration, WorkerRegistrationAdmin)
admin.site.register(ShiftType)
admin.site.register(ShiftSubType)
admin.site.register(Shift, ShiftAdmin)
