# encoding: utf-8
from django.contrib import admin
from .models import Ticket, TicketType

admin.site.register(Ticket)
admin.site.register(TicketType)
