# encoding: utf-8
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm

from django.utils.translation import ugettext_lazy as _

from .models import Visitor, Ticket, TicketType


class VisitorChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = Visitor


class VisitorUserAdmin(UserAdmin):
    form = VisitorChangeForm

    fieldsets = UserAdmin.fieldsets + (
        (_('Additional info'), {'fields': ('pid',)}),
    )


admin.site.register(Visitor, VisitorUserAdmin)
admin.site.register(Ticket)
admin.site.register(TicketType)
