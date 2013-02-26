# encoding: utf-8
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm

from django.utils.translation import ugettext_lazy as _

from .models import ShiftType, ShiftSubType, Shift, Worker, WorkerRegistration


class WorkerChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = Worker


class WorkerUserAdmin(UserAdmin):
    form = WorkerChangeForm

    fieldsets = UserAdmin.fieldsets + (
        (_('Additional info'), {'fields': ('pid',)}),
    )

class WorkerRegistrationAdmin(ModelAdmin):
    pass

class ShiftAdmin(admin.ModelAdmin):
    list_select_related = True


admin.site.register(Worker, WorkerUserAdmin)
admin.site.register(WorkerRegistration)
admin.site.register(ShiftType)
admin.site.register(ShiftSubType)
admin.site.register(Shift, ShiftAdmin)
