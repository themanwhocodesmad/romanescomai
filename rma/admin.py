from django.contrib import admin
from .models import RMA

@admin.register(RMA)
class RMAAdmin(admin.ModelAdmin):
    list_display = (
        'rma_number',
        'service_centre',
        'date_returned',
        'company_name',
        'contact_person',
        'contact_number',
        'email_address',
        'inv_no',
        'inv_date',
        'item_code',
        'action',
        'reason',
        'customer_name'
    )
    search_fields = (
        'rma_number',
        'service_centre',
        'company_name',
        'contact_person',
        'contact_number',
        'email_address',
        'inv_no',
        'item_code',
        'action',
        'reason',
        'customer_name'
    )
    list_filter = ('date_returned', 'action')
    date_hierarchy = 'date_returned'
