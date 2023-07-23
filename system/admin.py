from django.contrib import admin
from .models import Customer, JobCounter, JobCard, Image


# Define Inline Image model for JobCard
class ImageInline(admin.TabularInline):
    model = Image
    extra = 1


# Define JobCardAdmin
class JobCardAdmin(admin.ModelAdmin):
    list_display = ['job_number', 'customer', 'product_name', 'job_status', 'sla_status', 'assigned_date',
                    'completed_date']
    list_filter = ['job_status', 'priority', 'job_type']
    search_fields = ['job_number', 'customer__name', 'product_name', 'job_status']
    inlines = [ImageInline]  # This will allow to manage Images directly from the JobCard interface


admin.site.register(JobCard, JobCardAdmin)


# Define ImageAdmin
class ImageAdmin(admin.ModelAdmin):
    list_display = ['job_card', 'description']
    list_filter = ['job_card']
    search_fields = ['job_card__job_number']


admin.site.register(Image, ImageAdmin)


# Define CustomerAdmin
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'contact_number', 'alt_contact_number', 'address']
    search_fields = ['name', 'email', 'contact_number']


admin.site.register(Customer, CustomerAdmin)


# Define JobCounterAdmin
class JobCounterAdmin(admin.ModelAdmin):
    list_display = ['counter']


admin.site.register(JobCounter, JobCounterAdmin)
