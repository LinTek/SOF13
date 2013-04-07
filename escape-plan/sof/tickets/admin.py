# encoding: utf-8
from django.contrib import admin
from .models import Ticket, TicketType


class TicketAdmin(admin.ModelAdmin):
    search_fields = ('invoice__ocr', 'invoice__person__liu_id', 'invoice__person__pid')

admin.site.register(Ticket, TicketAdmin)
admin.site.register(TicketType)
