from django.contrib import admin

from .models import ShiftType, Shift, Functionary

admin.site.register(ShiftType)
admin.site.register(Shift)
admin.site.register(Functionary)
