from django.contrib import admin
from .models import Invoice


class InvoiceAdmin(admin.ModelAdmin):
    search_fields = ['invoice_id', 'user']
    list_display = ('invoice_id', 'user', 'payment_method', 'cost', 'status')


admin.site.register(Invoice, InvoiceAdmin)
