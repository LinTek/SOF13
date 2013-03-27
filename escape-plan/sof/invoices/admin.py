from django.contrib import admin

from django.utils.translation import ugettext_lazy as _

from .models import Invoice, Payment


admin.site.register(Invoice)
admin.site.register(Payment)
