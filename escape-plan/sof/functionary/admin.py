# encoding: utf-8
from django.contrib import admin

from .models import (ShiftType, ShiftSubType, Shift, Worker, WorkerRegistration,
                     Person, Visitor)


class WorkerRegistrationAdmin(admin.ModelAdmin):
    list_select_related = True
    list_display = ('worker', 'shift')
    search_fields = ('worker__first_name', 'worker__last_name', 'worker__username')


class ShiftAdmin(admin.ModelAdmin):
    list_select_related = True
    list_display = ('shift_type', 'shift_sub_type',
                    'start', 'end', 'max_workers')
    search_fields = ('shift_type__name', 'shift_sub_type__name')


admin.site.register(Person)
admin.site.register(Visitor)
admin.site.register(Worker)
admin.site.register(WorkerRegistration, WorkerRegistrationAdmin)
admin.site.register(ShiftType)
admin.site.register(ShiftSubType)
admin.site.register(Shift, ShiftAdmin)
