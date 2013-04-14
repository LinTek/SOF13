from django.contrib import admin

from .models import Invoice, SpecialInvoice, Payment


class InvoiceAdmin(admin.ModelAdmin):
    search_fields = ('ocr', 'person__pid', 'person__liu_id',
                     'person__first_name', 'person__last_name')


class SpecialInvoiceAdmin(admin.ModelAdmin):
    search_fields = ('ocr', 'person__pid', 'person__liu_id',
                     'person__first_name', 'person__last_name')


class PaymentAdmin(admin.ModelAdmin):
    search_fields = ('amount', 'invoice__ocr')

admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(SpecialInvoice, SpecialInvoiceAdmin)
admin.site.register(Payment, PaymentAdmin)
